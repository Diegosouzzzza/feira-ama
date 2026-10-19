from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from fastapi import Request
from starlette.requests import HTTPConnection

from amazonvision.config import Settings
from amazonvision.core.bus import EventBus
from amazonvision.core.clock import to_db, utc_now
from amazonvision.core.control import ControlManager
from amazonvision.schemas.api import EventSource, Severity, SystemStatus
from amazonvision.schemas.events import SnapshotEvent
from amazonvision.services.lots import LotService
from amazonvision.services.status import StatusService
from amazonvision.storage.db import Database
from amazonvision.storage.events import add_event


@dataclass
class Services:
    settings: Settings
    db: Database
    bus: EventBus
    control: ControlManager
    lots: LotService
    status: StatusService

    @classmethod
    def create(cls, settings: Settings) -> "Services":
        db = Database(settings.db_path)
        bus = EventBus()
        control = ControlManager(ttl=timedelta(minutes=settings.control_ttl_minutes))
        return cls(
            settings=settings,
            db=db,
            bus=bus,
            control=control,
            lots=LotService(settings, db, bus),
            status=StatusService(settings, db, control),
        )

    async def start(self) -> None:
        await self.db.open()

    async def stop(self) -> None:
        await self.db.close()

    async def current_status(self) -> SystemStatus:
        return await self.status.build(self.bus.state_version)

    async def snapshot(self) -> SnapshotEvent:
        seq, version = self.bus.seq, self.bus.state_version
        status = await self.status.build(version)
        return self.bus.snapshot(status, seq=seq, state_version=version)

    async def resync_all(self) -> None:
        """State changed outside the event stream (e.g. control holder): resend snapshots."""
        self.bus.bump_version()
        self.bus.broadcast(await self.snapshot())

    async def record(
        self,
        type: str,
        *,
        severity: Severity = Severity.INFO,
        source: EventSource = EventSource.OPERATOR,
        data: dict[str, Any] | None = None,
        lot_id: int | None = None,
    ) -> None:
        now = to_db(utc_now())
        await self.db.run(
            lambda conn: add_event(
                conn,
                source=source,
                type=type,
                severity=severity,
                occurred_at=now,
                data=data,
                lot_id=lot_id,
            )
        )


def get_services(conn: HTTPConnection) -> Services:
    return conn.app.state.services


def services_dep(request: Request) -> Services:
    return get_services(request)
