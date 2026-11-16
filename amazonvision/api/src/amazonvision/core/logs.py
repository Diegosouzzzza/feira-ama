import json
import logging
import logging.handlers
from datetime import UTC, datetime
from pathlib import Path

LOG_FILE = "amazonvision.jsonl"


class JsonLinesFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            entry["exc"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False)


def setup_logging(log_dir: Path | None, level: int = logging.INFO) -> None:
    """Console (human) + optional rotating JSON Lines file under the data directory."""
    root = logging.getLogger()
    root.setLevel(level)
    for handler in list(root.handlers):
        root.removeHandler(handler)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
    root.addHandler(console)

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(JsonLinesFormatter())
        root.addHandler(file_handler)
