"""What the simulated bench will 'see'. Shared by the simulated camera (draws the item) and the
stub classifier (returns its scores), so image and prediction stay consistent."""

import random
from collections import deque
from dataclasses import dataclass

from amazonvision.domain.quality import Grade


@dataclass(frozen=True)
class PlannedItem:
    label: str
    scores: dict[Grade, float] | None

    @property
    def drawn_as(self) -> str:
        if self.scores is None:
            return "empty"
        return max(self.scores, key=lambda g: self.scores[g]).value  # type: ignore[index]


def confident(grade: Grade, confidence: float = 0.92) -> PlannedItem:
    rest = (1.0 - confidence) / 2
    scores = {g: (confidence if g is grade else rest) for g in Grade}
    return PlannedItem(label=grade.value, scores=scores)


def uncertain(top: Grade = Grade.A, top_score: float = 0.55) -> PlannedItem:
    others = [g for g in Grade if g is not top]
    second = (1.0 - top_score) * 0.75
    scores = {top: top_score, others[0]: second, others[1]: 1.0 - top_score - second}
    return PlannedItem(label="incerto", scores=scores)


def invalid_image() -> PlannedItem:
    return PlannedItem(label="invalida", scores=None)


class Scenario:
    """Queue of planned items; when empty, draws a plausible random mix."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._queue: deque[PlannedItem] = deque()

    def push(self, *items: PlannedItem) -> None:
        self._queue.extend(items)

    def clear(self) -> None:
        self._queue.clear()

    def next(self) -> PlannedItem:
        if self._queue:
            return self._queue.popleft()
        roll = self._rng.random()
        if roll < 0.65:
            return confident(Grade.A, self._rng.uniform(0.85, 0.98))
        if roll < 0.80:
            return confident(Grade.B, self._rng.uniform(0.82, 0.96))
        if roll < 0.90:
            return confident(Grade.C, self._rng.uniform(0.82, 0.96))
        if roll < 0.98:
            return uncertain(self._rng.choice(list(Grade)), self._rng.uniform(0.45, 0.7))
        return invalid_image()
