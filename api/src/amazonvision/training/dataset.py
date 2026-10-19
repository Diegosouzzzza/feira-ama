"""Dataset manifest and the split by physical sample (photos of one piece never cross splits).

manifest.csv columns: path, product_id, physical_sample_id, label, split (split may be empty)."""

import csv
import random
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, replace
from pathlib import Path

from amazonvision.domain.quality import Grade

SPLITS = ("train", "val", "test")
FIELDS = ("path", "product_id", "physical_sample_id", "label", "split")


@dataclass(frozen=True)
class Sample:
    path: str
    product_id: str
    physical_sample_id: str
    label: Grade
    split: str = ""


def read_manifest(path: Path) -> list[Sample]:
    with open(path, encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    samples = []
    for i, row in enumerate(rows, start=2):
        try:
            samples.append(
                Sample(
                    path=row["path"],
                    product_id=row["product_id"],
                    physical_sample_id=row["physical_sample_id"],
                    label=Grade(row["label"]),
                    split=row.get("split") or "",
                )
            )
        except (KeyError, ValueError) as exc:
            raise ValueError(f"linha {i} do manifesto inválida: {exc}") from exc
    return samples


def write_manifest(path: Path, samples: Iterable[Sample]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for s in samples:
            writer.writerow(
                {
                    "path": s.path,
                    "product_id": s.product_id,
                    "physical_sample_id": s.physical_sample_id,
                    "label": s.label.value,
                    "split": s.split,
                }
            )


def split_by_physical_sample(
    samples: list[Sample],
    *,
    seed: int = 7,
    ratios: tuple[float, float, float] = (0.70, 0.15, 0.15),
) -> list[Sample]:
    """Assign train/val/test per physical sample, stratified by label.

    Every photo of the same piece lands in the same split, so the test set measures pieces the
    model never saw. Each label gets at least one piece in val and in test when it has 3+ pieces."""
    groups: dict[str, list[Sample]] = defaultdict(list)
    for s in samples:
        groups[s.physical_sample_id].append(s)
    by_label: dict[Grade, list[str]] = defaultdict(list)
    for sample_id, items in groups.items():
        labels = {s.label for s in items}
        if len(labels) != 1:
            raise ValueError(f"amostra física {sample_id} tem fotos com rótulos diferentes")
        by_label[items[0].label].append(sample_id)

    rng = random.Random(seed)
    assignment: dict[str, str] = {}
    for label in sorted(by_label):
        ids = sorted(by_label[label])
        rng.shuffle(ids)
        n = len(ids)
        n_val = max(1, round(n * ratios[1])) if n >= 3 else 0
        n_test = max(1, round(n * ratios[2])) if n >= 3 else 0
        for i, sample_id in enumerate(ids):
            if i < n_test:
                assignment[sample_id] = "test"
            elif i < n_test + n_val:
                assignment[sample_id] = "val"
            else:
                assignment[sample_id] = "train"
    return [replace(s, split=assignment[s.physical_sample_id]) for s in samples]


def check_no_leakage(samples: list[Sample]) -> None:
    seen: dict[str, str] = {}
    for s in samples:
        if s.split not in SPLITS:
            raise ValueError(f"{s.path}: partição ausente ou inválida")
        previous = seen.setdefault(s.physical_sample_id, s.split)
        if previous != s.split:
            raise ValueError(
                f"amostra física {s.physical_sample_id} aparece em mais de uma partição"
            )
