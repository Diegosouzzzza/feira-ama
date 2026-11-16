"""Image preprocessing shared by training and inference (the same function on both sides).

The frame is letterboxed, never stretched, so defects near the edges are kept. An optional ROI
(region of interest) crops the frame to the inspection window before the letterbox, so the model
never has to learn to ignore belt and background; it is set per product and baked into the
trained model's package, so training and inference always agree on it."""

import io
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
from PIL import Image

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


@dataclass(frozen=True)
class RoiSpec:
    """Crop window as fractions (0..1) of the frame, origin at the top-left corner."""

    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        for name, value in (("x", self.x), ("y", self.y)):
            if not 0 <= value < 1:
                raise ValueError(f"roi.{name} deve estar entre 0 e 1 (exclusivo)")
        for name, value, origin in (
            ("width", self.width, self.x),
            ("height", self.height, self.y),
        ):
            if not 0 < value <= 1 - origin:
                raise ValueError(f"roi.{name} deve caber no quadro a partir de x/y")

    def to_dict(self) -> dict[str, float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RoiSpec":
        return cls(
            x=float(data["x"]),
            y=float(data["y"]),
            width=float(data["width"]),
            height=float(data["height"]),
        )

    def crop(self, image: Image.Image) -> Image.Image:
        left = round(self.x * image.width)
        top = round(self.y * image.height)
        right = max(left + 1, round((self.x + self.width) * image.width))
        bottom = max(top + 1, round((self.y + self.height) * image.height))
        return image.crop((left, top, min(right, image.width), min(bottom, image.height)))


@dataclass(frozen=True)
class PreprocessSpec:
    input_size: int = 224
    mean: tuple[float, float, float] = IMAGENET_MEAN
    std: tuple[float, float, float] = IMAGENET_STD
    resize: str = "letterbox"
    pad_rgb: tuple[int, int, int] = field(default=(124, 116, 104))  # mean colour: neutral pad
    roi: RoiSpec | None = None  # None: the whole frame, as captured

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.roi is None:
            data.pop("roi")
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PreprocessSpec":
        if data.get("resize", "letterbox") != "letterbox":
            raise ValueError(f"pré-processamento desconhecido: {data.get('resize')}")
        roi = data.get("roi")
        return cls(
            input_size=int(data["input_size"]),
            mean=tuple(data["mean"]),  # type: ignore[arg-type]
            std=tuple(data["std"]),  # type: ignore[arg-type]
            resize="letterbox",
            pad_rgb=tuple(data.get("pad_rgb", (124, 116, 104))),  # type: ignore[arg-type]
            roi=RoiSpec.from_dict(roi) if roi else None,
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
    rgb = image.convert("RGB")
    if spec.roi is not None:
        rgb = spec.roi.crop(rgb)
    boxed = letterbox(rgb, spec)
    array = np.asarray(boxed, dtype=np.float32) / 255.0
    array = (array - np.array(spec.mean, dtype=np.float32)) / np.array(spec.std, dtype=np.float32)
    return np.ascontiguousarray(array.transpose(2, 0, 1))


def prepare_bytes(data: bytes, spec: PreprocessSpec) -> np.ndarray:
    return prepare_image(load_rgb(data), spec)
