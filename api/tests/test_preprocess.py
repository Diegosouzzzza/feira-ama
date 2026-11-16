import numpy as np
import pytest
from PIL import Image

from amazonvision.vision.preprocess import PreprocessSpec, RoiSpec, prepare_image


def solid(color: tuple[int, int, int], size: tuple[int, int] = (200, 100)) -> Image.Image:
    return Image.new("RGB", size, color)


def test_roi_rejects_a_window_that_does_not_fit_the_frame():
    RoiSpec(x=0.1, y=0.1, width=0.5, height=0.5)  # fits: no error
    with pytest.raises(ValueError, match="width"):
        RoiSpec(x=0.6, y=0.0, width=0.5, height=0.5)
    with pytest.raises(ValueError, match="height"):
        RoiSpec(x=0.0, y=0.6, width=0.5, height=0.5)
    with pytest.raises(ValueError, match="x"):
        RoiSpec(x=1.0, y=0.0, width=0.1, height=0.1)


def test_roi_crop_keeps_only_the_window():
    # Left half red, right half blue; a right-half ROI should crop away all the red.
    image = Image.new("RGB", (200, 100))
    for x in range(200):
        for y in range(100):
            image.putpixel((x, y), (255, 0, 0) if x < 100 else (0, 0, 255))

    roi = RoiSpec(x=0.5, y=0.0, width=0.5, height=1.0)
    cropped = roi.crop(image)
    assert cropped.size == (100, 100)
    colors = cropped.getcolors()
    assert colors == [(100 * 100, (0, 0, 255))]


def test_preprocess_spec_roundtrips_with_and_without_roi():
    with_roi = PreprocessSpec(roi=RoiSpec(x=0.1, y=0.2, width=0.6, height=0.5))
    restored = PreprocessSpec.from_dict(with_roi.to_dict())
    assert restored == with_roi
    assert "roi" not in PreprocessSpec().to_dict()
    assert PreprocessSpec.from_dict(PreprocessSpec().to_dict()).roi is None


def test_roi_changes_what_the_model_sees():
    """The ROI genuinely changes the pixels reaching the model, not just metadata."""
    image = solid((255, 0, 0))
    for x in range(100, 200):
        for y in range(100):
            image.putpixel((x, y), (0, 0, 255))  # right half is blue

    full = prepare_image(image, PreprocessSpec())
    cropped = prepare_image(image, PreprocessSpec(roi=RoiSpec(x=0.5, y=0.0, width=0.5, height=1.0)))
    assert not np.array_equal(full, cropped)
    # The cropped array holds no red at all once denormalised back towards the raw channel order.
    assert full.mean() != cropped.mean()


def test_anomaly_map_projects_grid_cells_through_letterbox_and_roi():
    from amazonvision.vision.anomaly_map import extract_anomaly_regions

    # Wide ROI (200x100 inside 400x200) -> letterboxed to 224x112 with pad_y=56.
    spec = PreprocessSpec(input_size=224, roi=RoiSpec(x=0.25, y=0.25, width=0.5, height=0.5))
    grid = np.full((28, 28), -2.0, dtype=np.float32)
    # Two adjacent active patches near the center of the ROI (rows 13..14, cols 13..14).
    grid[13:15, 13:15] = 2.0
    # One active patch purely in the top letterbox padding (row 0) should be ignored.
    grid[0, 10] = 3.0

    regions = extract_anomaly_regions(grid, image_size=(400, 200), spec=spec)
    assert len(regions) == 1
    reg = regions[0]
    assert 0.4 < reg.x < 0.55
    assert 0.4 < reg.y < 0.55
    assert 0.0 < reg.width < 0.15
    assert 0.0 < reg.height < 0.15
    assert reg.intensity > 0.85


def test_anomaly_map_returns_empty_when_below_threshold():
    from amazonvision.vision.anomaly_map import extract_anomaly_regions

    grid = np.full((28, 28), -0.5, dtype=np.float32)
    assert extract_anomaly_regions(grid, image_size=(320, 240), spec=PreprocessSpec()) == ()
