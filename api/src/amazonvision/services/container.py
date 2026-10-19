from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from fastapi import Request
from starlette.requests import HTTPConnection

from amazonvision.camera.base import Camera, NoCamera
from amazonvision.camera.simulated import SimulatedCamera
from amazonvision.config import RunMode, Settings
from amazonvision.core.bus import EventBus
from amazonvision.core.clock import to_db, utc_now
from amazonvision.core.control import ControlManager
from amazonvision.machine.coordinator import Coordinator
from amazonvision.machine.link import Link
from amazonvision.machine.process_link import ProcessLink
from amazonvision.machine.simulated_device import SimulatedDevice
from amazonvision.schemas.api import EventSource, Severity, SystemStatus
from amazonvision.schemas.events import SnapshotEvent
from amazonvision.services.lots import LotService
from amazonvision.services.models import ModelService
from amazonvision.services.reviews import ReviewService
from amazonvision.services.status import StatusService
from amazonvision.simulation.scenario import Scenario
from amazonvision.storage.db import Database
from amazonvision.storage.events import add_event
from amazonvision.vision.classifier import ModelManager


@dataclass
class Simulation:
    """Handles to the simulated bench (simulated mode only): scenario and fault injection."""

    camera: SimulatedCamera
    scenario: Scenario
    device: SimulatedDevice | None = None  # Python simulator of the board
    native: ProcessLink | None = None  # or the firmware logic compiled for the PC


class Recorder:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def __call__(
        self,
        type: str,
        *,
        severity: Severity = Severity.INFO,
        source: EventSource = EventSource.OPERATOR,
        data: dict[str, Any] | None = None,
        lot_id: int | None = None,
    ) -> None:
        now = to_db(utc_now())
        await self._db.run(
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


@dataclass
class Services:
    settings: Settings
    db: Database
    bus: EventBus
    control: ControlManager
    models: ModelManager
    camera: Camera
    coordinator: Coordinator
    lots: LotService
    reviews: ReviewService
    model_registry: ModelService
    status: StatusService
    record: Recorder
    simulation: Simulation | None

    @classmethod
    def create(cls, settings: Settings) -> "Services":
        db = Database(settings.db_path)
        bus = EventBus()
        control = ControlManager(ttl=timedelta(minutes=settings.control_ttl_minutes))
        models = ModelManager(settings)
        record = Recorder(db)

        simulation: Simulation | None = None
        link: Link | None = None
        camera: Camera = NoCamera()
        port_label: str | None = None
        if settings.mode is RunMode.SIMULADO:
            scenario = Scenario(settings.sim_seed)
            sim_camera = SimulatedCamera(scenario)
            camera = sim_camera
            if settings.firmware_harness:
                native = ProcessLink(settings.firmware_harness)
                simulation = Simulation(camera=sim_camera, scenario=scenario, native=native)
                link, port_label = native, "firmware nativo"
            else:
                device = SimulatedDevice(speed=settings.sim_speed)
                simulation = Simulation(camera=sim_camera, scenario=scenario, device=device)
                link, port_label = device, "simulador"
        # Real mode: serial link (Block 6) and real camera (Block 7) are not wired yet.

        coordinator = Coordinator(settings, db, bus, link, camera, models, record, port_label)
        lots = LotService(
            settings,
            db,
            bus,
            machine_busy=coordinator.busy,
            on_opened=lambda lot: models.load(lot.product_id, lot.model_id),
            on_closed=lambda lot: models.unload(),
        )
        services = cls(
            settings=settings,
            db=db,
            bus=bus,
            control=control,
            models=models,
            camera=camera,
            coordinator=coordinator,
            lots=lots,
            reviews=ReviewService(db, bus, coordinator),
            model_registry=ModelService(settings, db),
            status=StatusService(settings, db, control, coordinator, camera, models),
            record=record,
            simulation=simulation,
        )
        coordinator.on_change = services.resync_all
        return services

    async def start(self) -> None:
        await self.db.open()
        await self.coordinator.start()

    async def stop(self) -> None:
        await self.coordinator.stop()
        await self.db.close()

    async def current_status(self) -> SystemStatus:
        return await self.status.build(self.bus.state_version)

    async def snapshot(self) -> SnapshotEvent:
        seq, version = self.bus.seq, self.bus.state_version
        status = await self.status.build(version)
        return self.bus.snapshot(status, seq=seq, state_version=version)

    async def resync_all(self) -> None:
        """State changed outside the event stream: resend a full snapshot to every client."""
        self.bus.bump_version()
        if self.bus.subscriber_count:
            self.bus.broadcast(await self.snapshot())


def get_services(conn: HTTPConnection) -> Services:
    return conn.app.state.services


def services_dep(request: Request) -> Services:
    return get_services(request)
