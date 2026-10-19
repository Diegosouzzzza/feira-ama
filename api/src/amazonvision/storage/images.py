"""Inspection images on disk. Written atomically; the database only points to complete files."""

import hashlib
import os
from pathlib import Path


def save_image(
    data_root: Path, lot_id: int, cycle_id: int, data: bytes, extension: str
) -> tuple[str, str]:
    """Write images/<lot>/<cycle>.<ext> atomically. Returns (relative posix path, sha256)."""
    relative = Path("images") / str(lot_id) / f"{cycle_id}.{extension}"
    target = data_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"imagem do ciclo {cycle_id} já existe")
    write_atomic(target, data)
    return relative.as_posix(), hashlib.sha256(data).hexdigest()


def write_atomic(target: Path, data: bytes) -> None:
    """Write to a temporary file, flush to disk, then rename: readers never see a partial file."""
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    with open(temporary, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)


def resolve_image(data_root: Path, relative: str) -> Path | None:
    root = data_root.resolve()
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        return None
    return candidate
