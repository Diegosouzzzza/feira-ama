"""Single-operator control lock. In memory: a service restart releases control."""

import secrets
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

from amazonvision.core.clock import utc_now
from amazonvision.schemas.errors import ApiError, ErrorCode


@dataclass
class Grant:
    token: str
    operator: str
    expires_at: datetime


class ClaimOutcome:
    NEW = "CONTROL_CLAIMED"
    RENEWED = "CONTROL_RENEWED"
    TAKEOVER = "CONTROL_TAKEOVER"


class ControlManager:
    def __init__(
        self, ttl: timedelta = timedelta(minutes=30), clock: Callable[[], datetime] = utc_now
    ) -> None:
        self._ttl = ttl
        self._clock = clock
        self._grant: Grant | None = None

    def _active(self) -> Grant | None:
        if self._grant is not None and self._grant.expires_at <= self._clock():
            self._grant = None
        return self._grant

    @property
    def holder(self) -> str | None:
        grant = self._active()
        return grant.operator if grant else None

    def _matches(self, token: str | None) -> bool:
        grant = self._active()
        return bool(token) and grant is not None and secrets.compare_digest(grant.token, token)

    def claim(
        self, operator: str, *, takeover: bool = False, token: str | None = None
    ) -> tuple[Grant, str, str | None]:
        """Returns (grant, outcome, previous_holder)."""
        current = self._active()
        expires_at = self._clock() + self._ttl
        if current is not None and self._matches(token):
            current.operator = operator
            current.expires_at = expires_at
            return current, ClaimOutcome.RENEWED, None
        if current is not None and not takeover:
            raise ApiError(
                ErrorCode.CONTROL_LOCKED,
                f"O controle da estação está com {current.operator}.",
                "Peça para liberar o controle ou assuma o controle.",
            )
        previous = current.operator if current else None
        self._grant = Grant(secrets.token_urlsafe(24), operator, expires_at)
        outcome = ClaimOutcome.TAKEOVER if previous else ClaimOutcome.NEW
        return self._grant, outcome, previous

    def verify(self, token: str | None) -> Grant:
        """Check the token and slide its expiry. Raises CONTROL_LOCKED otherwise."""
        if not self._matches(token):
            holder = self.holder
            message = (
                f"O controle da estação está com {holder}."
                if holder
                else "Esta tela não tem o controle da estação."
            )
            raise ApiError(ErrorCode.CONTROL_LOCKED, message, "Assuma o controle para operar.")
        assert self._grant is not None
        self._grant.expires_at = self._clock() + self._ttl
        return self._grant

    def release(self, token: str | None) -> str:
        grant = self.verify(token)
        self._grant = None
        return grant.operator
