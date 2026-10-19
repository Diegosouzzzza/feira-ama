import time
from dataclasses import dataclass
from typing import Protocol

from amazonvision.camera.base import Frame
from amazonvision.config import RunMode, Settings
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import ModelInfo
from amazonvision.simulation.scenario import PlannedItem


class ClassifierError(Exception):
    pass


@dataclass(frozen=True)
class Prediction:
    scores: dict[Grade, float] | None  # None: image unusable
    latency_ms: float


class Classifier(Protocol):
    product_id: str
    model_id: str | None

    def classify(self, frame: Frame) -> Prediction:
        """Blocking; runs on the inference thread."""
        ...


class StubClassifier:
    """Simulation only: returns the scores planned for the simulated item in the frame."""

    model_id = None

    def __init__(self, product_id: str) -> None:
        self.product_id = product_id

    def classify(self, frame: Frame) -> Prediction:
        started = time.perf_counter()
        item = frame.meta.get("sim_item")
        if not isinstance(item, PlannedItem):
            raise ClassifierError("quadro sem item simulado")
        return Prediction(scores=item.scores, latency_ms=(time.perf_counter() - started) * 1000)


class ModelManager:
    """Holds the classifier for the open lot's product."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self.classifier: Classifier | None = None
        self._product_id: str | None = None

    def load(self, product_id: str) -> None:
        self._product_id = product_id
        if self._settings.mode is RunMode.SIMULADO:
            self.classifier = StubClassifier(product_id)
        else:
            # Real ONNX models arrive in Block 8.
            self.classifier = None

    def unload(self) -> None:
        self.classifier = None
        self._product_id = None

    def ready_for(self, product_id: str) -> bool:
        return self.classifier is not None and self.classifier.product_id == product_id

    def info(self) -> ModelInfo:
        if self.classifier is not None:
            return ModelInfo(
                status="ready", model_id=self.classifier.model_id, product_id=self._product_id
            )
        return ModelInfo(status="not_loaded", model_id=None, product_id=self._product_id)
