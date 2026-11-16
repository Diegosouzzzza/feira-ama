import asyncio
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi.responses import Response

from amazonvision.camera import probe as camera_probe
from amazonvision.camera.opencv_camera import is_device_index
from amazonvision.machine.serial_link import list_ports
from amazonvision.routes.deps import ServicesDep
from amazonvision.schemas.api import (
    CameraDeviceOut,
    CameraDiagnostics,
    EventOut,
    EventSource,
    SerialPortOut,
    Severity,
)
from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.services.container import Services
from amazonvision.storage.events import list_events

router = APIRouter(prefix="/diagnostics", tags=["diagnóstico"])


@router.get("/serial-ports", response_model=list[SerialPortOut])
async def serial_ports(services: ServicesDep) -> list[SerialPortOut]:
    """Portas USB visíveis ao sistema agora, para escolher em AV_SERIAL_PORT."""
    in_use = services.settings.serial_port
    return [SerialPortOut(**port, in_use=port["device"] == in_use) for port in list_ports()]


def _index_in_use(services: Services) -> int | None:
    source = services.settings.camera_source
    return int(source) if source and is_device_index(source) else None


def _refuse_while_running(services: Services) -> None:
    # Opening other cameras costs USB bandwidth and CPU: never during an inspection.
    if services.coordinator.busy():
        raise ApiError(
            ErrorCode.INVALID_STATE,
            "A esteira está em operação.",
            "Pare a máquina antes de testar as câmeras.",
        )


@router.get("/cameras", response_model=CameraDiagnostics)
async def cameras(
    services: ServicesDep,
    max_index: Annotated[int, Query(ge=1, le=10, description="Quantos índices testar")] = 6,
) -> CameraDiagnostics:
    """Câmeras visíveis ao sistema agora, para escolher AV_CAMERA_SOURCE.

    Abre cada índice por um instante (alguns segundos no total). O índice que a bancada já
    está usando não é reaberto. Use `snapshot_url` para ver qual é a webcam do notebook e qual
    é a webcam virtual do celular (DroidCam/Iriun)."""
    _refuse_while_running(services)
    settings = services.settings
    in_use = _index_in_use(services)
    skip = frozenset() if in_use is None else frozenset({in_use})
    probed = await asyncio.to_thread(camera_probe.probe_indexes, max_index, skip=skip)
    devices = [
        CameraDeviceOut(
            index=int(result.source),
            available=result.available,
            width=result.width,
            height=result.height,
            in_use=False,
            snapshot_url=(
                f"/api/diagnostics/cameras/{result.source}/snapshot" if result.available else None
            ),
        )
        for result in probed
    ]
    info = services.camera.info()
    if in_use is not None and in_use < max_index:
        devices.append(
            CameraDeviceOut(
                index=in_use,
                available=info.status == "ok",
                width=None,
                height=None,
                in_use=True,
                snapshot_url="/api/camera/snapshot",
            )
        )
        devices.sort(key=lambda device: device.index)
    source = settings.camera_source
    kind = "none" if not source else ("index" if is_device_index(source) else "stream")
    return CameraDiagnostics(
        configured_source=source,
        source_kind=kind,
        rotate=settings.camera_rotate,
        capture_timeout_s=settings.camera_capture_timeout_s,
        camera=info,
        devices=devices,
        guide=camera_probe.GUIDE.splitlines(),
    )


@router.get(
    "/cameras/{index}/snapshot",
    responses={200: {"content": {"image/jpeg": {}}}},
    response_class=Response,
)
async def camera_snapshot(
    services: ServicesDep, index: Annotated[int, Path(ge=0, le=9)]
) -> Response:
    """Foto do que a câmera deste índice está vendo agora (abre no navegador)."""
    if index == _index_in_use(services):
        latest = await services.camera.preview()
        data = latest[0] if latest else None
    else:
        _refuse_while_running(services)
        result = await asyncio.to_thread(
            camera_probe.probe, str(index), rotate=services.settings.camera_rotate
        )
        data = result.jpeg
    if data is None:
        raise ApiError(
            ErrorCode.CAMERA_UNAVAILABLE,
            f"A câmera {index} não entregou imagem.",
            "Confira se o app do celular está conectado e se outro programa não a está usando.",
        )
    return Response(data, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@router.get("/events", response_model=list[EventOut])
async def events(
    services: ServicesDep,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    severity: Severity | None = None,
    source: EventSource | None = None,
    type: Annotated[
        str | None, Query(max_length=40, description="Ex.: FAULT, CONFIG_CHANGED")
    ] = None,
    lot_id: Annotated[int | None, Query(ge=1)] = None,
) -> list[EventOut]:
    return await services.db.run(
        lambda conn: list_events(
            conn,
            limit=limit,
            offset=offset,
            severity=severity,
            source=source,
            type=type,
            lot_id=lot_id,
        )
    )
