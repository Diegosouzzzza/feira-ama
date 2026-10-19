import logging
import time
from dataclasses import dataclass
from typing import Protocol

from amazonvision.camera.base import Frame
from amazonvision.config import RunMode, Settings
from amazonvision.domain.quality import Grade
from amazonvision.schemas.api import ModelInfo
from amazonvision.simulation.scenario import PlannedItem

log = logging.getLogger("amazonvision.models")


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
    """Holds the classifier for the open lot's product.

    A product with an installed, active model always uses it (ONNX). Without one, the simulated
    mode falls back to the stub; the real mode has no classifier and refuses to operate."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self.classifier: Classifier | None = None
        self._product_id: str | None = None
        self._error: str | None = None

    def load(self, product_id: str, model_id: str | None) -> None:
        from amazonvision.vision.onnx_classifier import OnnxClassifier
        from amazonvision.vision.package import PackageError, load_package

        self._product_id = product_id
        self._error = None
        self.classifier = None
        if model_id is not None:
            try:
                package = load_package(self._settings.data_root / "models" / model_id)
                if package.product_id != product_id:
                    raise PackageError("o modelo é de outro produto")
                self.classifier = OnnxClassifier(package)
            except (PackageError, OSError) as exc:
                self._error = str(exc)
                log.error("modelo %s não carregou: %s", model_id, exc)
        elif self._settings.mode is RunMode.SIMULADO:
            self.classifier = StubClassifier(product_id)

    def unload(self) -> None:
        self.classifier = None
        self._product_id = None
        self._error = None

    def ready_for(self, product_id: str) -> bool:
        return self.classifier is not None and self.classifier.product_id == product_id

    def info(self) -> ModelInfo:
        if self.classifier is not None:
            return ModelInfo(
                status="ready", model_id=self.classifier.model_id, product_id=self._product_id
            )
        if self._error is not None:
            return ModelInfo(status="error", model_id=None, product_id=self._product_id)
        return ModelInfo(status="not_loaded", model_id=None, product_id=self._product_id)
