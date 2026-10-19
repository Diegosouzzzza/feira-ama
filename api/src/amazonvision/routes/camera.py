import asyncio
from collections.abc import AsyncIterator

from fastapi import APIRouter, Request
from fastapi.responses import Response, StreamingResponse

from amazonvision.routes.deps import ServicesDep
from amazonvision.schemas.errors import ApiError, ErrorCode

router = APIRouter(prefix="/camera", tags=["câmera"])

BOUNDARY = "avframe"
PREVIEW_FPS = 5


@router.get("/snapshot", responses={200: {"content": {"image/jpeg": {}}}})
async def snapshot(services: ServicesDep) -> Response:
    """Imagem mais recente da câmera (visualização; não é uma foto de inspeção)."""
    latest = await services.camera.preview()
    if latest is None:
        raise ApiError(ErrorCode.CAMERA_UNAVAILABLE, "Câmera sem imagem.")
    data, media_type = latest
    return Response(data, media_type=media_type, headers={"Cache-Control": "no-store"})


@router.get("/stream", responses={200: {"content": {"multipart/x-mixed-replace": {}}}})
async def stream(request: Request, services: ServicesDep) -> StreamingResponse:
    """Vídeo ao vivo (MJPEG). Canal separado das mensagens de estado da máquina."""

    async def frames() -> AsyncIterator[bytes]:
        while not await request.is_disconnected():
            latest = await services.camera.preview()
            if latest is not None:
                data, media_type = latest
                yield (
                    (
                        f"--{BOUNDARY}\r\nContent-Type: {media_type}\r\n"
                        f"Content-Length: {len(data)}\r\n\r\n"
                    ).encode()
                    + data
                    + b"\r\n"
                )
            await asyncio.sleep(1 / PREVIEW_FPS)

    return StreamingResponse(
        frames(),
        media_type=f"multipart/x-mixed-replace; boundary={BOUNDARY}",
        headers={"Cache-Control": "no-store"},
    )
