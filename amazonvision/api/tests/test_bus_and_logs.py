import json
import logging
from datetime import UTC, datetime

from amazonvision.core.bus import EventBus
from amazonvision.core.logs import JsonLinesFormatter
from amazonvision.schemas.events import ConnectionData, ConnectionLostEvent

AT = datetime(2026, 10, 18, 12, 0, tzinfo=UTC)


def lost() -> ConnectionData:
    return ConnectionData(component="device", message="ESP32 sem resposta")


def test_publish_increments_seq_and_version():
    bus = EventBus(clock=lambda: AT)
    sub = bus.subscribe()
    first = bus.publish(ConnectionLostEvent, lost())
    second = bus.publish(ConnectionLostEvent, lost(), changes_state=False)
    assert (first.seq, first.state_version) == (1, 1)
    assert (second.seq, second.state_version) == (2, 1)
    assert sub.queue.get_nowait() is first
    assert sub.queue.get_nowait() is second


def test_slow_subscriber_is_flagged_not_blocking():
    bus = EventBus(clock=lambda: AT, queue_size=2)
    slow = bus.subscribe()
    fast = bus.subscribe()
    for _ in range(3):
        bus.publish(ConnectionLostEvent, lost())
        while not fast.queue.empty():
            fast.queue.get_nowait()
    assert slow.lagged is True
    assert fast.lagged is False


def test_unsubscribed_clients_receive_nothing():
    bus = EventBus(clock=lambda: AT)
    sub = bus.subscribe()
    bus.unsubscribe(sub)
    bus.publish(ConnectionLostEvent, lost())
    assert sub.queue.empty()
    assert bus.subscriber_count == 0


def test_json_lines_formatter_is_one_json_object_per_record():
    record = logging.LogRecord(
        "amazonvision", logging.WARNING, __file__, 1, "câmera %s", ("ok",), None
    )
    line = JsonLinesFormatter().format(record)
    data = json.loads(line)
    assert "\n" not in line
    assert data["level"] == "WARNING"
    assert data["msg"] == "câmera ok"
    assert data["ts"].endswith("+00:00")
