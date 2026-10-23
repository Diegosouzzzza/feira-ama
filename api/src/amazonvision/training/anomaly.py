"""Anomaly detection trained on good pieces only (memory bank of patch features, PatchCore-style).

When no defective pieces exist yet, the model learns only what a good piece looks like: every small
patch of a new photo is compared with the patches seen on good pieces, and a photo whose patches
are far from all of them is "out of standard". Spots, mould, dark areas, missing pieces and odd
shapes all show up as distance, without the model ever seeing them.

The package is an ordinary A/B/C model: the ONNX graph turns the distance into logits
[A = within standard, B = never, C = out of standard], so the API, the decision policy and the
bench run it unchanged. Between the two edges the confidence falls below the threshold and the
piece goes to human review.

Its limits are written in the report: without real defective pieces nobody can measure how many
defects it catches, and it is sensitive to the imaging setup (background, light, camera), so it
must be rebuilt with photos of good pieces taken on the bench itself."""

import json
import math
import random
import time
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torch import nn
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

from amazonvision.domain.quality import Grade
from amazonvision.training.dataset import (
    Sample,
    check_no_leakage,
    read_manifest,
    split_by_physical_sample,
    write_manifest,
)
from amazonvision.training.evaluate import classification_metrics, policy_metrics
from amazonvision.training.report import write_anomaly_report
from amazonvision.vision.onnx_classifier import OnnxClassifier
from amazonvision.vision.package import FORMAT_VERSION, WEIGHTS, load_package, sha256_file
from amazonvision.vision.package import write_manifest as write_model_manifest
from amazonvision.vision.preprocess import PreprocessSpec, RoiSpec, prepare_image

ARCHITECTURE = "anomalia_patchcore_mobilenet_v3_small"
NEVER_LOGIT = -30.0  # class B: this model never predicts it (softmax ≈ 1e-13)
APPROVE_QUANTILE = 0.95  # good validation pieces at or below this score are approved outright
REJECT_SPREAD = 2.0  # reject edge = approve edge + this many standard deviations of good scores
MAX_BANK_CANDIDATES = 200_000


class PatchFeatures(nn.Module):
    """Mid-level features of a pretrained MobileNetV3 Small, one vector per 8x8 pixel patch.

    Two depths are combined (stride 8 and 16, averaged over a 3x3 neighbourhood): fine enough for
    small spots, deep enough to ignore pixel noise."""

    def __init__(self, pretrained: bool = True) -> None:
        super().__init__()
        weights = MobileNet_V3_Small_Weights.IMAGENET1K_V1 if pretrained else None
        features = mobilenet_v3_small(weights=weights).features
        self.low = features[:4]  # stride 8, 24 channels
        self.mid = features[4:9]  # stride 16, 48 channels

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        low = self.low(x)
        mid = self.mid(low)
        low = F.avg_pool2d(low, kernel_size=3, stride=1, padding=1)
        mid = F.avg_pool2d(mid, kernel_size=3, stride=1, padding=1)
        mid = F.interpolate(mid, size=low.shape[-2:], mode="bilinear", align_corners=False)
        return torch.cat([low, mid], dim=1).flatten(2).transpose(1, 2)  # (batch, patches, 72)


class AnomalyScorer(nn.Module):
    """Photo -> logits [A, B, C]. With center=0 and scale=1 the C logit is the raw distance."""

    def __init__(
        self,
        features: PatchFeatures,
        bank: torch.Tensor,
        *,
        center: float = 0.0,
        scale: float = 1.0,
        top_k: int = 3,
    ) -> None:
        super().__init__()
        self.features = features
        self.register_buffer("bank", bank)
        self.register_buffer("bank_sq", (bank * bank).sum(dim=1))
        self.center = center
        self.scale = scale
        self.top_k = top_k

    def distance(self, x: torch.Tensor) -> torch.Tensor:
        patches = self.features(x)[0]
        squared = (
            (patches * patches).sum(dim=1, keepdim=True)
            - 2 * patches @ self.bank.T
            + self.bank_sq[None, :]
        )
        nearest = torch.sqrt(torch.clamp(squared.min(dim=1).values, min=0.0))
        # Mean of the few worst patches: one bad patch matters, one noisy pixel does not.
        return torch.topk(nearest, self.top_k).values.mean()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        z = (self.distance(x) - self.center) / self.scale
        return torch.stack([torch.zeros_like(z), torch.full_like(z, NEVER_LOGIT), z])[None, :]


def _views(image: Image.Image) -> list[Image.Image]:
    """The piece can land in any orientation on the belt: all 8 rotations/mirrors are 'good'."""
    out = []
    for flipped in (image, image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)):
        out += [flipped.rotate(angle, expand=True) for angle in (0, 90, 180, 270)]
    return out


def _coreset(candidates: torch.Tensor, size: int, seed: int) -> torch.Tensor:
    """Greedy k-center subset: keeps the variety of the patches with a fraction of them."""
    generator = torch.Generator().manual_seed(seed)
    if len(candidates) > MAX_BANK_CANDIDATES:
        keep = torch.randperm(len(candidates), generator=generator)[:MAX_BANK_CANDIDATES]
        candidates = candidates[keep]
    if len(candidates) <= size:
        return candidates
    first = int(torch.randint(len(candidates), (1,), generator=generator))
    chosen = [first]
    nearest = ((candidates - candidates[first]) ** 2).sum(dim=1)
    for _ in range(size - 1):
        index = int(torch.argmax(nearest))
        chosen.append(index)
        nearest = torch.minimum(nearest, ((candidates - candidates[index]) ** 2).sum(dim=1))
    return candidates[chosen]


def _load(root: Path, sample: Sample) -> Image.Image:
    with Image.open(root / sample.path) as raw:
        return raw.convert("RGB")


def build_bank(
    features: PatchFeatures,
    root: Path,
    samples: list[Sample],
    spec: PreprocessSpec,
    *,
    size: int,
    seed: int,
) -> torch.Tensor:
    patches = []
    with torch.no_grad():
        for sample in samples:
            for view in _views(_load(root, sample)):
                array = prepare_image(view, spec)
                patches.append(features(torch.from_numpy(array)[None])[0])
    return _coreset(torch.cat(patches), size, seed)


def calibrate(good_scores: list[float], threshold: float) -> dict[str, float]:
    """Turn distances of good validation pieces into the two decision edges.

    approve_edge: most good pieces score below it -> confidence in A reaches the threshold there.
    reject_edge: well above the good pieces -> confidence in C reaches the threshold there.
    Between them the piece goes to review. Without defective pieces, the reject edge is a
    statistical guess; recalibrating on the bench with real pieces is part of the procedure."""
    values = np.array(good_scores, dtype=np.float64)
    approve = float(np.quantile(values, APPROVE_QUANTILE))
    spread = float(values.std()) or 0.1 * approve or 1.0
    reject = approve + REJECT_SPREAD * spread
    center = (approve + reject) / 2
    scale = (center - approve) / math.log(threshold / (1 - threshold))
    return {
        "approve_edge": approve,
        "reject_edge": reject,
        "center": center,
        "scale": scale,
        "good_median": float(np.median(values)),
        "good_max": float(values.max()),
    }


def _export_onnx(model: nn.Module, spec: PreprocessSpec, path: Path) -> None:
    model = model.cpu().eval()
    dummy = torch.zeros(1, 3, spec.input_size, spec.input_size)
    torch.onnx.export(
        model,
        (dummy,),
        str(path),
        input_names=["image"],
        output_names=["logits"],
        opset_version=18,
        dynamo=True,
        external_data=False,
    )


def _distances(scorer: AnomalyScorer, root: Path, samples: list[Sample], spec: PreprocessSpec):
    with torch.no_grad():
        return [
            float(scorer.distance(torch.from_numpy(prepare_image(_load(root, s), spec))[None]))
            for s in samples
        ]


def _onnx_scores(classifier: OnnxClassifier, root: Path, samples: list[Sample]):
    y_true, scores, latencies = [], [], []
    for sample in samples:
        array = prepare_image(_load(root, sample), classifier.package.preprocess)
        started = time.perf_counter()
        scores.append(classifier.classify_array(array))
        latencies.append((time.perf_counter() - started) * 1000)
        y_true.append(sample.label)
    return y_true, scores, latencies


def _percentile(values: list[float], q: float) -> float | None:
    return float(np.percentile(np.array(values), q)) if values else None


def train_anomaly(
    manifest_path: Path,
    *,
    product_id: str,
    out_dir: Path,
    pretrained: bool = True,
    bank_size: int = 4000,
    threshold: float = 0.80,
    seed: int = 7,
    dataset_version: str | None = None,
    roi: RoiSpec | None = None,
) -> Path:
    """Build, calibrate, export and evaluate an anomaly model. Returns the package folder.

    Pieces labelled A are the good ones: they are split by physical piece into the bank (train),
    calibration (val) and the false-alarm measurement (test). Pieces labelled B or C are optional
    known anomalies and only ever go to the test set."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    root = manifest_path.parent
    rows = [s for s in read_manifest(manifest_path) if s.product_id == product_id]
    good = [s for s in rows if s.label is Grade.A]
    if len({s.physical_sample_id for s in good}) < 3:
        raise ValueError(f"o produto {product_id} precisa de pelo menos 3 peças boas (classe A)")
    good = split_by_physical_sample([replace(s, split="") for s in good], seed=seed)
    anomalies = [replace(s, split="test") for s in rows if s.label is not Grade.A]
    samples = good + anomalies
    check_no_leakage(samples)
    parts = {name: [s for s in samples if s.split == name] for name in ("train", "val", "test")}

    created = datetime.now(UTC)
    model_id = f"{product_id}-anomalia-{created:%Y%m%d-%H%M%S}"
    package_dir = out_dir / model_id
    package_dir.mkdir(parents=True, exist_ok=False)
    write_manifest(package_dir / "dataset_split.csv", samples)

    spec = PreprocessSpec(roi=roi)
    features = PatchFeatures(pretrained).eval()
    bank = build_bank(features, root, parts["train"], spec, size=bank_size, seed=seed)

    raw = AnomalyScorer(features, bank).eval()
    val_distances = _distances(raw, root, parts["val"], spec)
    edges = calibrate(val_distances, threshold)
    scorer = AnomalyScorer(features, bank, center=edges["center"], scale=edges["scale"]).eval()

    onnx_path = package_dir / WEIGHTS
    _export_onnx(scorer, spec, onnx_path)
    manifest: dict[str, Any] = {
        "format_version": FORMAT_VERSION,
        "model_id": model_id,
        "product_id": product_id,
        "architecture": ARCHITECTURE,
        "class_order": [g.value for g in (Grade.A, Grade.B, Grade.C)],
        "preprocess": spec.to_dict(),
        "dataset_version": dataset_version or f"{manifest_path.name}@{created:%Y-%m-%d}",
        "weights_sha256": sha256_file(onnx_path),
        "recommended_threshold": threshold,
        "metrics": {},
        "created_at": created.isoformat(),
    }
    write_model_manifest(package_dir, manifest)
    classifier = OnnxClassifier(load_package(package_dir))

    # The exported graph must give the same answer as the PyTorch one.
    max_diff = 0.0
    with torch.no_grad():
        for sample in parts["val"][:8]:
            array = prepare_image(_load(root, sample), spec)
            expected = torch.softmax(scorer(torch.from_numpy(array)[None]), dim=1)[0].numpy()
            got = classifier.classify_array(array)
            max_diff = max(max_diff, abs(float(expected[2]) - got[Grade.C]))

    y_test, s_test, latencies = _onnx_scores(classifier, root, parts["test"])
    test_distances = _distances(raw, root, parts["test"], spec)
    good_test = [
        d for d, s in zip(test_distances, parts["test"], strict=True) if s.label is Grade.A
    ]
    odd_test = [
        d for d, s in zip(test_distances, parts["test"], strict=True) if s.label is not Grade.A
    ]
    metrics: dict[str, Any] = {
        "kind": "anomalia",
        "split_sizes": {
            name: {"photos": len(p), "pieces": len({s.physical_sample_id for s in p})}
            for name, p in parts.items()
        },
        "known_anomalies": len(anomalies),
        "bank": {"patches": int(bank.shape[0]), "dims": int(bank.shape[1]), "views_per_photo": 8},
        "calibration": {**edges, "threshold": threshold, "val_good_pieces": len(val_distances)},
        "distances": {
            "test_good": {"median": _percentile(good_test, 50), "max": _percentile(good_test, 100)},
            "test_known_anomalies": {
                "median": _percentile(odd_test, 50),
                "min": _percentile(odd_test, 0),
            },
        },
        "export_max_prob_diff": max_diff,
        "pretrained": pretrained,
        "seed": seed,
        "test": {
            **classification_metrics(y_test, s_test),
            "policy": policy_metrics(y_test, s_test, threshold),
            "latency_ms": {"p50": _percentile(latencies, 50), "p95": _percentile(latencies, 95)},
        },
    }
    policy = metrics["test"]["policy"]
    # The package's architecture tells the screens it is an anomaly model; metrics stay numeric.
    manifest["metrics"] = {
        "test_good_rejected_rate": policy["good_wrongly_rejected_rate"],
        "test_review_rate": policy["review_rate"],
        "test_known_anomalies_rejected_rate": policy["defective_rejected_rate"],
        "test_known_anomalies_approved_rate": policy["defective_false_approval_rate"],
        "latency_p95_ms": metrics["test"]["latency_ms"]["p95"],
        # Never "ready" on its own: no real defective piece was ever measured.
        "ready_for_bench": False,
    }
    write_model_manifest(package_dir, manifest)
    (package_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", "utf-8"
    )
    write_anomaly_report(package_dir / "relatorio.md", manifest, metrics)
    return package_dir
