"""Project spatial patch anomaly maps back onto original image coordinates."""

from collections import deque
from dataclasses import dataclass

import numpy as np

from amazonvision.vision.preprocess import PreprocessSpec


@dataclass(frozen=True)
class AnomalyRegion:
    """Normalized bounding box (0..1) on the full captured frame, with peak intensity (0..1)."""

    x: float
    y: float
    width: float
    height: float
    intensity: float


def _sigmoid(z: float) -> float:
    if z >= 0:
        return float(1.0 / (1.0 + np.exp(-z)))
    exp_z = float(np.exp(z))
    return exp_z / (1.0 + exp_z)


def _crop_box(
    image_size: tuple[int, int], spec: PreprocessSpec
) -> tuple[float, float, float, float, int, int]:
    orig_w, orig_h = image_size
    if spec.roi is None:
        return 0.0, 0.0, 1.0, 1.0, max(1, orig_w), max(1, orig_h)
    roi = spec.roi
    left = round(roi.x * orig_w)
    top = round(roi.y * orig_h)
    right = min(orig_w, max(left + 1, round((roi.x + roi.width) * orig_w)))
    bottom = min(orig_h, max(top + 1, round((roi.y + roi.height) * orig_h)))
    return roi.x, roi.y, roi.width, roi.height, max(1, right - left), max(1, bottom - top)


def _connected_boxes(
    active: np.ndarray, patch_z: np.ndarray
) -> list[tuple[int, int, int, int, float]]:
    rows, cols = active.shape
    visited = np.zeros_like(active, dtype=bool)
    boxes: list[tuple[int, int, int, int, float]] = []

    for start_r in range(rows):
        for start_c in range(cols):
            if not active[start_r, start_c] or visited[start_r, start_c]:
                continue
            queue: deque[tuple[int, int]] = deque([(start_r, start_c)])
            visited[start_r, start_c] = True
            min_r = max_r = start_r
            min_c = max_c = start_c
            peak_z = float(patch_z[start_r, start_c])

            while queue:
                r, c = queue.popleft()
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
                val = float(patch_z[r, c])
                if val > peak_z:
                    peak_z = val
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and active[nr, nc]
                            and not visited[nr, nc]
                        ):
                            visited[nr, nc] = True
                            queue.append((nr, nc))

            boxes.append((min_r, min_c, max_r + 1, max_c + 1, _sigmoid(peak_z)))
    return boxes


def extract_anomaly_regions(
    patch_z: np.ndarray,
    *,
    image_size: tuple[int, int],
    spec: PreprocessSpec,
    z_threshold: float = 0.0,
    max_regions: int = 5,
) -> tuple[AnomalyRegion, ...]:
    """Turn a standardized (grid_h, grid_w) patch_z map into full-frame normalized boxes."""
    if patch_z.ndim != 2 or patch_z.size == 0:
        return ()
    rows, cols = patch_z.shape
    active = patch_z >= z_threshold
    if not np.any(active):
        return ()

    roi_x, roi_y, roi_w, roi_h, crop_w, crop_h = _crop_box(image_size, spec)
    size = spec.input_size
    scale = min(size / crop_w, size / crop_h)
    new_w = max(1, round(crop_w * scale))
    new_h = max(1, round(crop_h * scale))
    pad_x = (size - new_w) // 2
    pad_y = (size - new_h) // 2

    regions: list[AnomalyRegion] = []
    for r0, c0, r1, c1, intensity in _connected_boxes(active, patch_z):
        x0_canvas = (c0 / cols) * size
        x1_canvas = (c1 / cols) * size
        y0_canvas = (r0 / rows) * size
        y1_canvas = (r1 / rows) * size

        x0_crop = min(1.0, max(0.0, (x0_canvas - pad_x) / new_w))
        x1_crop = min(1.0, max(0.0, (x1_canvas - pad_x) / new_w))
        y0_crop = min(1.0, max(0.0, (y0_canvas - pad_y) / new_h))
        y1_crop = min(1.0, max(0.0, (y1_canvas - pad_y) / new_h))
        if x1_crop <= x0_crop or y1_crop <= y0_crop:
            continue

        regions.append(
            AnomalyRegion(
                x=roi_x + x0_crop * roi_w,
                y=roi_y + y0_crop * roi_h,
                width=(x1_crop - x0_crop) * roi_w,
                height=(y1_crop - y0_crop) * roi_h,
                intensity=intensity,
            )
        )

    regions.sort(key=lambda reg: (reg.intensity, reg.width * reg.height), reverse=True)
    return tuple(regions[:max_regions])
