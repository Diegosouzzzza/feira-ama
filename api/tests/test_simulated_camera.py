"""Simulated camera with a folder of real photos (AV_SIM_PHOTOS)."""

import io
from datetime import UTC, datetime
from pathlib import Path

import pytest
from PIL import Image

from amazonvision.camera.simulated import SimulatedCamera, list_photos
from amazonvision.simulation.scenario import Scenario

pytestmark = pytest.mark.anyio


def _photo(path: Path, colour: tuple[int, int, int]) -> None:
    Image.new("RGB", (64, 48), colour).save(path)


async def test_real_photos_are_shown_one_per_piece_as_distinct_jpegs(tmp_path: Path):
    _photo(tmp_path / "a.jpg", (200, 120, 60))
    _photo(tmp_path / "b.png", (90, 60, 30))
    (tmp_path / "notas.txt").write_text("não é foto", encoding="utf-8")
    photos = list_photos(tmp_path)
    assert [p.name for p in photos] == ["a.jpg", "b.png"]

    camera = SimulatedCamera(Scenario(seed=1), photos=photos, seed=1)
    since = datetime(2026, 10, 21, tzinfo=UTC)
    frames = [await camera.capture(since, timeout_s=1) for _ in range(4)]

    assert all(f.media_type == "image/jpeg" and f.extension == "jpg" for f in frames)
    # Every photo is used before any repeats, and repeated photos are still distinct files.
    assert {f.meta["sim_photo"] for f in frames[:2]} == {"a.jpg", "b.png"}
    assert len({f.data for f in frames}) == 4
    with Image.open(io.BytesIO(frames[0].data)) as image:
        assert image.size == (64, 48)

    preview = await camera.preview()
    assert preview is not None and preview[1] == "image/jpeg"


def test_empty_folder_is_reported(tmp_path: Path):
    with pytest.raises(ValueError, match="nenhuma foto"):
        list_photos(tmp_path)
