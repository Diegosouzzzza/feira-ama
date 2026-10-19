"""In-process event bus feeding the WebSocket. Runs on the event loop thread only."""

import asyncio
from collections.abc import Callable
from datetime import datetime
from typing import Any

from amazonvision.core.clock import utc_now
from amazonvision.schemas.api import SystemStatus
from amazonvision.schemas.events import SnapshotEvent


class Subscription:
    def __init__(self, maxsize: int) -> None:
        self.queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=maxsize)
        self.lagged = False

    def offer(self, event: Any) -> None:
        if self.lagged:
            return
        try:
            self.queue.put_nowait(event)
        except asyncio.QueueFull:
            # The client is too slow; it will be disconnected and resync with a new snapshot.
            self.lagged = True


class EventBus:
    def __init__(self, clock: Callable[[], datetime] = utc_now, queue_size: int = 256) -> None:
        self._clock = clock
        self._queue_size = queue_size
        self._seq = 0
        self._state_version = 0
        self._subs: set[Subscription] = set()

    @property
    def seq(self) -> int:
        return self._seq

    @property
    def state_version(self) -> int:
        return self._state_version

    @property
    def subscriber_count(self) -> int:
        return len(self._subs)

    def subscribe(self) -> Subscription:
        sub = Subscription(self._queue_size)
        self._subs.add(sub)
        return sub

    def unsubscribe(self, sub: Subscription) -> None:
        self._subs.discard(sub)

    def bump_version(self) -> int:
        self._state_version += 1
        return self._state_version

    def publish(
        self,
        event_cls: type,
        data: Any,
        *,
        lot_id: int | None = None,
        cycle_id: int | None = None,
        changes_state: bool = True,
    ) -> Any:
        self._seq += 1
        if changes_state:
            self._state_version += 1
        event = event_cls(
            seq=self._seq,
            at=self._clock(),
            state_version=self._state_version,
            lot_id=lot_id,
            cycle_id=cycle_id,
            data=data,
        )
        for sub in list(self._subs):
            sub.offer(event)
        return event

    def snapshot(self, status: SystemStatus, *, seq: int, state_version: int) -> SnapshotEvent:
        """Build a snapshot. seq/state_version must be captured *before* reading the state."""
        return SnapshotEvent(seq=seq, at=self._clock(), state_version=state_version, data=status)

    def broadcast(self, snapshot: SnapshotEvent) -> None:
        for sub in list(self._subs):
            sub.offer(snapshot)
