"""Quality policy: model scores -> automatic decision. Pure, no I/O.

The model prediction and the operational decision are different things; both are stored.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType


class Grade(StrEnum):
    A = "A"
    B = "B"
    C = "C"


class Destination(StrEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AutoDecision(StrEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"


class ReviewReason(StrEnum):
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    AMBIGUOUS = "AMBIGUOUS"
    INVALID_IMAGE = "INVALID_IMAGE"


DEFAULT_DESTINATIONS: Mapping[Grade, Destination] = MappingProxyType(
    {Grade.A: Destination.APPROVED, Grade.B: Destination.REJECTED, Grade.C: Destination.REJECTED}
)

_SCORE_SUM_TOLERANCE = 1e-3


@dataclass(frozen=True)
class QualityPolicy:
    threshold: float
    destinations: Mapping[Grade, Destination] = field(default=DEFAULT_DESTINATIONS)
    version: str = "v1"

    def __post_init__(self) -> None:
        if not 0.0 < self.threshold <= 1.0:
            raise ValueError("threshold deve estar em (0, 1]")
        if set(self.destinations) != set(Grade):
            raise ValueError("destinations deve mapear todas as classes A, B e C")


@dataclass(frozen=True)
class PolicyResult:
    predicted_grade: Grade | None
    confidence: float | None
    decision: AutoDecision
    review_reason: ReviewReason | None = None


def _validate_scores(scores: Mapping[Grade, float]) -> None:
    if set(scores) != set(Grade):
        raise ValueError("scores deve ter exatamente as classes A, B e C")
    values = list(scores.values())
    if any(not math.isfinite(v) or v < 0.0 or v > 1.0 for v in values):
        raise ValueError("cada score deve estar em [0, 1]")
    if abs(sum(values) - 1.0) > _SCORE_SUM_TOLERANCE:
        raise ValueError("scores devem somar 1 (saída softmax)")


def decide(scores: Mapping[Grade, float] | None, policy: QualityPolicy) -> PolicyResult:
    """Apply the policy. `scores=None` means the image was unusable (stale, empty, unreadable)."""
    if scores is None:
        return PolicyResult(None, None, AutoDecision.REVIEW, ReviewReason.INVALID_IMAGE)

    _validate_scores(scores)
    ranked = sorted(Grade, key=lambda g: scores[g], reverse=True)
    top, runner_up = ranked[0], ranked[1]
    confidence = scores[top]

    if math.isclose(confidence, scores[runner_up], abs_tol=1e-9):
        return PolicyResult(top, confidence, AutoDecision.REVIEW, ReviewReason.AMBIGUOUS)
    if confidence < policy.threshold:
        return PolicyResult(top, confidence, AutoDecision.REVIEW, ReviewReason.LOW_CONFIDENCE)
    return PolicyResult(top, confidence, AutoDecision(policy.destinations[top].value))
