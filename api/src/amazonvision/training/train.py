"""Training of the A/B/C classifier (MobileNetV3 Small, transfer learning) and export to ONNX.

Requires the "training" dependency group (torch, torchvision). The evaluation always runs on the
exported ONNX model, i.e. exactly what the bench will execute."""

import copy
import json
import random
import statistics
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image, ImageEnhance
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

from amazonvision.domain.quality import Grade
from amazonvision.training.dataset import (
    Sample,
    check_no_leakage,
    read_manifest,
    split_by_physical_sample,
    write_manifest,
)
from amazonvision.training.evaluate import (
    ORDER,
    choose_threshold,
    classification_metrics,
    policy_metrics,
)
from amazonvision.training.report import readiness, write_report
from amazonvision.vision.onnx_classifier import OnnxClassifier
from amazonvision.vision.package import FORMAT_VERSION, WEIGHTS, load_package, sha256_file
from amazonvision.vision.package import write_manifest as write_model_manifest
from amazonvision.vision.preprocess import PreprocessSpec, prepare_image

ARCHITECTURE = "mobilenet_v3_small"
LABEL_INDEX = {g: i for i, g in enumerate(ORDER)}


class PhotoDataset(Dataset):
    def __init__(self, root: Path, samples: list[Sample], spec: PreprocessSpec, augment: bool):
        self.root = root
        self.samples = samples
        self.spec = spec
        self.augment = augment

    def __len__(self) -> int:
        return len(self.samples)

    def _augment(self, image: Image.Image) -> Image.Image:
        # Geometry and mild brightness only: colour is part of the quality signal.
        if random.random() < 0.5:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if random.random() < 0.5:
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        image = image.rotate(random.choice([0, 90, 180, 270]), expand=True)
        return ImageEnhance.Brightness(image).enhance(random.uniform(0.92, 1.08))

    def __getitem__(self, i: int) -> tuple[torch.Tensor, int]:
        sample = self.samples[i]
        with Image.open(self.root / sample.path) as raw:
            image = raw.convert("RGB")
        if self.augment:
            image = self._augment(image)
        return torch.from_numpy(prepare_image(image, self.spec)), LABEL_INDEX[sample.label]


def _device(choice: str) -> torch.device:
    if choice == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(choice)


def _build_model(pretrained: bool) -> nn.Module:
    weights = MobileNet_V3_Small_Weights.IMAGENET1K_V1 if pretrained else None
    model = mobilenet_v3_small(weights=weights)
    last = model.classifier[3]
    assert isinstance(last, nn.Linear)
    model.classifier[3] = nn.Linear(last.in_features, len(ORDER))
    return model


def _macro_f1(model: nn.Module, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    y_true: list[Grade] = []
    scores: list[dict[Grade, float]] = []
    with torch.no_grad():
        for images, labels in loader:
            probs = torch.softmax(model(images.to(device)), dim=1).cpu().numpy()
            for p, label in zip(probs, labels.tolist(), strict=True):
                y_true.append(ORDER[label])
                scores.append({g: float(p[i]) for i, g in enumerate(ORDER)})
    return classification_metrics(y_true, scores)["macro_f1"] if y_true else 0.0


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


def _onnx_scores(
    classifier: OnnxClassifier, root: Path, samples: list[Sample]
) -> tuple[list[Grade], list[dict[Grade, float]], list[float]]:
    y_true, scores, latencies = [], [], []
    for sample in samples:
        with Image.open(root / sample.path) as raw:
            array = prepare_image(raw.convert("RGB"), classifier.package.preprocess)
        started = time.perf_counter()
        scores.append(classifier.classify_array(array))
        latencies.append((time.perf_counter() - started) * 1000)
        y_true.append(sample.label)
    return y_true, scores, latencies


def _percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.percentile(np.array(values), q))


def train(
    manifest_path: Path,
    *,
    product_id: str,
    out_dir: Path,
    epochs: int = 12,
    batch_size: int = 16,
    learning_rate: float = 1e-3,
    pretrained: bool = True,
    seed: int = 7,
    device: str = "auto",
    max_false_approval: float = 0.05,
    dataset_version: str | None = None,
) -> Path:
    """Train, export, evaluate and write a complete model package. Returns its folder."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    root = manifest_path.parent
    samples = [s for s in read_manifest(manifest_path) if s.product_id == product_id]
    if not samples:
        raise ValueError(f"nenhuma foto do produto {product_id} no manifesto")
    if any(not s.split for s in samples):
        samples = split_by_physical_sample(samples, seed=seed)
    check_no_leakage(samples)
    parts = {name: [s for s in samples if s.split == name] for name in ("train", "val", "test")}
    for name, part in parts.items():
        if not part:
            raise ValueError(f"partição {name} vazia: colete mais amostras físicas por classe")

    created = datetime.now(UTC)
    model_id = f"{product_id}-{created:%Y%m%d-%H%M%S}"
    package_dir = out_dir / model_id
    package_dir.mkdir(parents=True, exist_ok=False)
    write_manifest(package_dir / "dataset_split.csv", samples)

    spec = PreprocessSpec()
    dev = _device(device)
    model = _build_model(pretrained).to(dev)
    train_loader = DataLoader(
        PhotoDataset(root, parts["train"], spec, augment=True), batch_size=batch_size, shuffle=True
    )
    val_loader = DataLoader(PhotoDataset(root, parts["val"], spec, augment=False), batch_size=32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    history: list[dict[str, float]] = []
    best_f1, best_state, best_epoch = -1.0, copy.deepcopy(model.state_dict()), 0
    for epoch in range(1, epochs + 1):
        model.train()
        losses = []
        for images, labels in train_loader:
            optimizer.zero_grad()
            loss = loss_fn(model(images.to(dev)), labels.to(dev))
            loss.backward()
            optimizer.step()
            losses.append(float(loss.item()))
        val_f1 = _macro_f1(model, val_loader, dev)
        history.append({"epoch": epoch, "loss": statistics.fmean(losses), "val_macro_f1": val_f1})
        if val_f1 > best_f1:
            best_f1, best_state, best_epoch = val_f1, copy.deepcopy(model.state_dict()), epoch
    model.load_state_dict(best_state)

    onnx_path = package_dir / WEIGHTS
    _export_onnx(model, spec, onnx_path)
    weights_sha = sha256_file(onnx_path)
    manifest: dict[str, Any] = {
        "format_version": FORMAT_VERSION,
        "model_id": model_id,
        "product_id": product_id,
        "architecture": ARCHITECTURE,
        "class_order": [g.value for g in ORDER],
        "preprocess": spec.to_dict(),
        "dataset_version": dataset_version or f"{manifest_path.name}@{created:%Y-%m-%d}",
        "weights_sha256": weights_sha,
        "recommended_threshold": None,
        "metrics": {},
        "created_at": created.isoformat(),
    }
    write_model_manifest(package_dir, manifest)

    classifier = OnnxClassifier(load_package(package_dir))

    # Exported model must match the trained one.
    check = parts["val"][: min(8, len(parts["val"]))]
    model.eval()
    max_diff = 0.0
    with torch.no_grad():
        for sample in check:
            with Image.open(root / sample.path) as raw:
                array = prepare_image(raw.convert("RGB"), spec)
            torch_probs = torch.softmax(model(torch.from_numpy(array)[None]), dim=1)[0].numpy()
            onnx_probs = classifier.classify_array(array)
            max_diff = max(
                max_diff, *(abs(float(torch_probs[i]) - onnx_probs[g]) for i, g in enumerate(ORDER))
            )

    y_val, s_val, _ = _onnx_scores(classifier, root, parts["val"])
    threshold, val_policy = choose_threshold(y_val, s_val, max_false_approval=max_false_approval)
    y_test, s_test, latencies = _onnx_scores(classifier, root, parts["test"])

    metrics: dict[str, Any] = {
        "split_sizes": {
            name: {"photos": len(p), "pieces": len({s.physical_sample_id for s in p})}
            for name, p in parts.items()
        },
        "training": {
            "epochs": epochs,
            "best_epoch": best_epoch,
            "pretrained": pretrained,
            "device": str(dev),
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "seed": seed,
            "history": history,
        },
        "export_max_prob_diff": max_diff,
        "validation": {**classification_metrics(y_val, s_val), "policy": val_policy},
        "test": {
            **classification_metrics(y_test, s_test),
            "policy": policy_metrics(y_test, s_test, threshold),
            "latency_ms": {"p50": _percentile(latencies, 50), "p95": _percentile(latencies, 95)},
        },
        "max_false_approval_target": max_false_approval,
    }
    manifest["recommended_threshold"] = threshold
    manifest["metrics"] = {
        "test_macro_f1": metrics["test"]["macro_f1"],
        "test_defective_false_approval_rate": metrics["test"]["policy"][
            "defective_false_approval_rate"
        ],
        "test_defective_rejected_rate": metrics["test"]["policy"]["defective_rejected_rate"],
        "test_review_rate": metrics["test"]["policy"]["review_rate"],
        "latency_p95_ms": metrics["test"]["latency_ms"]["p95"],
        "ready_for_bench": not readiness(metrics),
    }
    write_model_manifest(package_dir, manifest)  # weights unchanged: sha still valid
    (package_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", "utf-8"
    )
    write_report(package_dir / "relatorio.md", manifest, metrics)
    return package_dir
