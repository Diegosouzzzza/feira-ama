"""Synthetic dataset from the simulator's drawings. Only to exercise the pipeline end to end:
a model trained on it says nothing about real tucumã or castanha."""

import random
from pathlib import Path

from PIL import Image, ImageEnhance

from amazonvision.domain.quality import Grade
from amazonvision.simulation.images import render
from amazonvision.training.dataset import Sample, write_manifest
from amazonvision.vision.preprocess import load_rgb


def generate(
    out: Path, *, product_id: str, pieces_per_class: int, photos_per_piece: int, seed: int = 3
) -> Path:
    rng = random.Random(seed)
    images = out / "imagens"
    images.mkdir(parents=True, exist_ok=True)
    samples: list[Sample] = []
    for grade in Grade:
        for piece in range(pieces_per_class):
            sample_id = f"{grade.value}-{piece:03d}"
            base = load_rgb(render(grade.value, piece % 3))
            for photo in range(photos_per_piece):
                image: Image.Image = base.rotate(rng.choice([0, 90, 180, 270]), expand=True)
                image = ImageEnhance.Brightness(image).enhance(rng.uniform(0.9, 1.1))
                name = f"{sample_id}-{photo}.png"
                image.save(images / name)
                samples.append(
                    Sample(
                        path=f"imagens/{name}",
                        product_id=product_id,
                        physical_sample_id=sample_id,
                        label=grade,
                    )
                )
    manifest = out / "manifest.csv"
    write_manifest(manifest, samples)
    return manifest
