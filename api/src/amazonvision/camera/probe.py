"""Find out which camera is which: the notebook webcam, the phone's virtual webcam, a stream.

OpenCV numbers local cameras 0, 1, 2... without names, and the order changes with what is
plugged in. This opens each index for a moment and keeps one picture of what it sees, so the
right value for AV_CAMERA_SOURCE can be chosen by looking.

Also runs on its own, without the service:

    uv run python -m amazonvision.camera.probe
    uv run python -m amazonvision.camera.probe --url http://127.0.0.1:8080/video
"""

import argparse
import contextlib
import sys
import threading
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import cv2

from amazonvision.camera.opencv_camera import ROTATIONS, VideoSource, open_device
from amazonvision.config import data_base_dir

MAX_INDEX = 6
WARMUP_FRAMES = 5  # the first frames of a webcam are often black or badly exposed

Opener = Callable[[str], VideoSource]

# One probe at a time: two threads opening the same device make DirectShow fail randomly.
_lock = threading.Lock()


@dataclass(frozen=True)
class ProbeResult:
    source: str
    available: bool
    width: int | None = None
    height: int | None = None
    jpeg: bytes | None = None


def _default_opener(source: str) -> VideoSource:
    # Small request: this is only to recognise the picture, and it opens faster.
    return open_device(source, 640, 480, None)


def probe(source: str, *, rotate: int = 0, opener: Opener | None = None) -> ProbeResult:
    """Open one source, read a few frames and keep the last as JPEG."""
    with _lock:
        capture: VideoSource | None = None
        try:
            capture = (opener or _default_opener)(source)
            if not capture.isOpened():
                return ProbeResult(source=source, available=False)
            image = None
            for _ in range(WARMUP_FRAMES):
                ok, frame = capture.read()
                if ok and frame is not None:
                    image = frame
            if image is None:
                return ProbeResult(source=source, available=False)
        except Exception:
            return ProbeResult(source=source, available=False)
        finally:
            if capture is not None:
                with contextlib.suppress(Exception):
                    capture.release()
    if rotate in ROTATIONS:
        image = cv2.rotate(image, ROTATIONS[rotate])
    height, width = image.shape[:2]
    ok, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return ProbeResult(
        source=source,
        available=True,
        width=int(width),
        height=int(height),
        jpeg=buffer.tobytes() if ok else None,
    )


def probe_indexes(
    count: int = MAX_INDEX, *, skip: frozenset[int] = frozenset(), opener: Opener | None = None
) -> list[ProbeResult]:
    """Probe indexes 0..count-1, except the ones in `skip` (a camera the service is using)."""
    return [probe(str(index), opener=opener) for index in range(count) if index not in skip]


GUIDE = """\
Como escolher o AV_CAMERA_SOURCE (em api\\.env):

  Celular como webcam virtual (DroidCam ou Iriun, por USB ou Wi-Fi)
    Abra o app no celular e o cliente no Windows e deixe conectado. O celular aparece como mais
    uma câmera: em geral o índice 0 é a webcam do notebook e o celular é o 1 ou o 2. Confira
    pelas fotos acima e use, por exemplo, AV_CAMERA_SOURCE=1.
    Se a foto do índice for a tela de espera do app (logotipo), o celular não está conectado.

  Celular como stream (app IP Webcam), pelo cabo USB
    No celular: IP Webcam > Iniciar servidor (porta 8080). No Windows, com a depuração USB ligada:
        adb forward tcp:8080 tcp:8080
    e use AV_CAMERA_SOURCE=http://127.0.0.1:8080/video
    Teste: uv run python -m amazonvision.camera.probe --url http://127.0.0.1:8080/video
    O adb forward se perde quando o cabo é tirado: rode de novo depois de reconectar.

  Celular como stream, por Wi-Fi
    Use o endereço que o app mostra: AV_CAMERA_SOURCE=http://192.168.x.x:8080/video
    (DroidCam: http://192.168.x.x:4747/video). Pelo cabo é mais estável que por Wi-Fi.

  Imagem deitada? AV_CAMERA_ROTATE=90 (ou 180, 270): gira no sentido horário.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lista as câmeras e salva uma foto de cada.")
    parser.add_argument("--max", type=int, default=MAX_INDEX, help="quantos índices testar")
    parser.add_argument("--url", help="testa um stream (http://... ou rtsp://...)")
    parser.add_argument("--rotate", type=int, default=0, choices=(0, 90, 180, 270))
    parser.add_argument("--out", type=Path, default=data_base_dir() / "cameras")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    if args.url:
        print(f"Abrindo {args.url} ...")
        results = [probe(args.url, rotate=args.rotate)]
    else:
        print(f"Testando os índices 0 a {args.max - 1} (alguns segundos por câmera)...")
        results = [probe(str(i), rotate=args.rotate) for i in range(args.max)]

    found = 0
    for result in results:
        label = result.source if args.url else f"índice {result.source}"
        if not result.available:
            print(f"  {label}: sem câmera ou sem imagem")
            continue
        found += 1
        name = "stream.jpg" if args.url else f"camera-{result.source}.jpg"
        saved = ""
        if result.jpeg is not None:
            path = args.out / name
            path.write_bytes(result.jpeg)
            saved = f"  foto: {path}"
        print(f"  {label}: {result.width}x{result.height}{saved}")

    print()
    if found == 0 and args.url:
        print("O stream não abriu. Confira se o app do celular está transmitindo e o endereço.")
    elif found == 0:
        print("Nenhuma câmera encontrada. Outro programa pode estar usando-as (feche-o).")
    else:
        print(f"Abra as fotos em {args.out} para ver qual câmera é qual.")
    print()
    print(GUIDE)
    return 0 if found else 1


if __name__ == "__main__":
    sys.exit(main())
