"""Image preprocessing shared by training and inference (the same function on both sides).

The whole frame is letterboxed (never cropped) so defects near the edges are kept."""

import io
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
from PIL import Image

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


@dataclass(frozen=True)
class PreprocessSpec:
    input_size: int = 224
    mean: tuple[float, float, float] = IMAGENET_MEAN
    std: tuple[float, float, float] = IMAGENET_STD
    resize: str = "letterbox"
    pad_rgb: tuple[int, int, int] = field(default=(124, 116, 104))  # mean colour: neutral pad

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PreprocessSpec":
        if data.get("resize", "letterbox") != "letterbox":
            raise ValueError(f"pré-processamento desconhecido: {data.get('resize')}")
        return cls(
            input_size=int(data["input_size"]),
            mean=tuple(data["mean"]),  # type: ignore[arg-type]
            std=tuple(data["std"]),  # type: ignore[arg-type]
            resize="letterbox",
            pad_rgb=tuple(data.get("pad_rgb", (124, 116, 104))),  # type: ignore[arg-type]
        )


def load_rgb(data: bytes) -> Image.Image:
    with Image.open(io.BytesIO(data)) as image:
        return image.convert("RGB")


def letterbox(image: Image.Image, spec: PreprocessSpec) -> Image.Image:
    size = spec.input_size
    scale = min(size / image.width, size / image.height)
    width = max(1, round(image.width * scale))
    height = max(1, round(image.height * scale))
    resized = image.resize((width, height), Image.Resampling.BILINEAR)
    canvas = Image.new("RGB", (size, size), spec.pad_rgb)
    canvas.paste(resized, ((size - width) // 2, (size - height) // 2))
    return canvas


def prepare_image(image: Image.Image, spec: PreprocessSpec) -> np.ndarray:
    """RGB image -> float32 array (3, size, size), normalised. Used by training and inference."""
    boxed = letterbox(image.convert("RGB"), spec)
    array = np.asarray(boxed, dtype=np.float32) / 255.0
    array = (array - np.array(spec.mean, dtype=np.float32)) / np.array(spec.std, dtype=np.float32)
    return np.ascontiguousarray(array.transpose(2, 0, 1))


def prepare_bytes(data: bytes, spec: PreprocessSpec) -> np.ndarray:
    return prepare_image(load_rgb(data), spec)
