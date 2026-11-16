"""Synthetic PNG frames for the simulated camera. Pure Python: no imaging dependency."""

import random
import struct
import zlib
from functools import lru_cache

WIDTH, HEIGHT = 400, 300

_BELT = (214, 209, 196)
_BELT_STRIPE = (204, 199, 186)
_STYLES: dict[str, dict] = {
    "A": {"body": (176, 112, 52), "rx": 58, "ry": 40, "spots": 0, "spot": (0, 0, 0)},
    "B": {"body": (160, 100, 48), "rx": 58, "ry": 40, "spots": 5, "spot": (70, 42, 22)},
    "C": {"body": (92, 64, 40), "rx": 34, "ry": 22, "spots": 2, "spot": (40, 28, 18)},
}


def encode_png(width: int, height: int, rgb_rows: list[bytes]) -> bytes:
    raw = b"".join(b"\x00" + row for row in rgb_rows)

    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 6))
        + chunk(b"IEND", b"")
    )


@lru_cache(maxsize=32)
def render(drawn_as: str, variant: int) -> bytes:
    """Belt with one item drawn as grade A/B/C, or an empty belt ('empty')."""
    rng = random.Random(f"{drawn_as}-{variant}")
    style = _STYLES.get(drawn_as)
    k = WIDTH / 240  # item geometry is specified for a 240 px wide frame
    cx = WIDTH / 2 + rng.uniform(-12, 12) * k
    cy = HEIGHT / 2 + rng.uniform(-8, 8) * k
    spots = (
        [
            (
                cx + rng.uniform(-30, 30) * k,
                cy + rng.uniform(-18, 18) * k,
                rng.uniform(5, 9) * k,
            )
            for _ in range(style["spots"])
        ]
        if style
        else []
    )
    rx, ry = (style["rx"] * k, style["ry"] * k) if style else (1.0, 1.0)
    stripe = int(12 * k)
    rows = []
    for y in range(HEIGHT):
        row = bytearray()
        for x in range(WIDTH):
            color = _BELT_STRIPE if (x // stripe) % 2 else _BELT
            if style:
                dx, dy = (x - cx) / rx, (y - cy) / ry
                d = dx * dx + dy * dy
                if d <= 1.0:
                    shade = 1.0 - 0.35 * d
                    color = tuple(int(c * shade) for c in style["body"])
                    for sx, sy, sr in spots:
                        if (x - sx) ** 2 + (y - sy) ** 2 <= sr * sr:
                            color = style["spot"]
                elif d <= 1.18:
                    color = tuple(int(c * 0.82) for c in _BELT)
            row.extend(color)
        rows.append(bytes(row))
    return encode_png(WIDTH, HEIGHT, rows)
