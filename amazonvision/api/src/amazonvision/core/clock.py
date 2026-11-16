from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


def to_db(moment: datetime) -> str:
    """Format as the database timestamp: ISO-8601 UTC with milliseconds and Z."""
    if moment.tzinfo is None:
        raise ValueError("horário sem fuso não pode ser gravado")
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def from_db(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))
