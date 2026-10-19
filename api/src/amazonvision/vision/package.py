"""Model package on disk: model.onnx + model.json (manifest). Produced by training, consumed by
the API. The manifest pins everything inference must reproduce."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amazonvision.domain.quality import Grade
from amazonvision.vision.preprocess import PreprocessSpec

MANIFEST = "model.json"
WEIGHTS = "model.onnx"
FORMAT_VERSION = 1


class PackageError(Exception):
    pass


@dataclass(frozen=True)
class ModelPackage:
    root: Path
    model_id: str
    product_id: str
    architecture: str
    class_order: tuple[Grade, ...]
    preprocess: PreprocessSpec
    dataset_version: str
    weights_sha256: str
    recommended_threshold: float | None
    metrics: dict[str, Any]
    created_at: str

    @property
    def weights_path(self) -> Path:
        return self.root / WEIGHTS


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(root: Path, manifest: dict[str, Any]) -> None:
    (root / MANIFEST).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")


def load_package(root: Path, *, verify: bool = True) -> ModelPackage:
    manifest_path = root / MANIFEST
    if not manifest_path.is_file() or not (root / WEIGHTS).is_file():
        raise PackageError(f"pacote de modelo incompleto em {root}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if data.get("format_version") != FORMAT_VERSION:
            raise PackageError("versão do pacote de modelo não suportada")
        package = ModelPackage(
            root=root,
            model_id=str(data["model_id"]),
            product_id=str(data["product_id"]),
            architecture=str(data["architecture"]),
            class_order=tuple(Grade(c) for c in data["class_order"]),
            preprocess=PreprocessSpec.from_dict(data["preprocess"]),
            dataset_version=str(data["dataset_version"]),
            weights_sha256=str(data["weights_sha256"]),
            recommended_threshold=data.get("recommended_threshold"),
            metrics=dict(data.get("metrics") or {}),
            created_at=str(data["created_at"]),
        )
    except (KeyError, ValueError, TypeError) as exc:
        raise PackageError(f"manifesto inválido: {exc}") from exc
    if sorted(package.class_order) != sorted(Grade):
        raise PackageError("o modelo deve ter exatamente as classes A, B e C")
    if verify and sha256_file(package.weights_path) != package.weights_sha256:
        raise PackageError("os pesos não conferem com o manifesto (arquivo alterado ou corrompido)")
    return package
