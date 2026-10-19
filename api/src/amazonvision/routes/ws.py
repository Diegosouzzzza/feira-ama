import asyncio
import contextlib
import logging
from urllib.parse import urlsplit

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from amazonvision.schemas.events import EventType
from amazonvision.services.container import get_services

log = logging.getLogger("amazonvision.ws")
router = APIRouter()

CLOSE_POLICY = 1008
CLOSE_RESYNC = 4000  # client fell behind: reconnect to get a fresh snapshot


def _origin_allowed(ws: WebSocket, allowed_hosts: list[str]) -> bool:
    """Browsers always send Origin; block pages from other sites reading the event stream."""
    origin = ws.headers.get("origin")
    if origin is None:
        return True
    host = urlsplit(origin).hostname or ""
    return host in {h.strip("[]") for h in allowed_hosts}


async def _wait_client_gone(ws: WebSocket) -> None:
    with contextlib.suppress(WebSocketDisconnect):
        while True:
            await ws.receive_text()


@router.websocket("/events")
async def events(ws: WebSocket) -> None:
    services = get_services(ws)
    if not _origin_allowed(ws, services.settings.allowed_hosts):
        await ws.close(code=CLOSE_POLICY)
        return
    await ws.accept()
    sub = services.bus.subscribe()
    gone = asyncio.create_task(_wait_client_gone(ws))
    try:
        snapshot = await services.snapshot()
        await ws.send_text(snapshot.model_dump_json())
        last_seq = snapshot.seq
        while True:
            next_event = asyncio.create_task(sub.queue.get())
            done, _ = await asyncio.wait({next_event, gone}, return_when=asyncio.FIRST_COMPLETED)
            if gone in done:
                next_event.cancel()
                return
            if sub.lagged:
                await ws.close(code=CLOSE_RESYNC, reason="resync")
                return
            event = next_event.result()
            if event.type is EventType.SNAPSHOT:
                last_seq = event.seq
            elif event.seq <= last_seq:
                continue  # already reflected in the snapshot this client received
            else:
                last_seq = event.seq
            await ws.send_text(event.model_dump_json())
    except WebSocketDisconnect:
        return
    finally:
        services.bus.unsubscribe(sub)
        gone.cancel()
