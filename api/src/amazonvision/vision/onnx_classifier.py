import time

import numpy as np
import onnxruntime as ort

from amazonvision.camera.base import Frame
from amazonvision.domain.quality import Grade
from amazonvision.vision.classifier import ClassifierError, Prediction
from amazonvision.vision.package import ModelPackage
from amazonvision.vision.preprocess import prepare_bytes


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max()
    exp = np.exp(shifted)
    return exp / exp.sum()


class OnnxClassifier:
    """Runs a validated model package on the CPU (ONNX Runtime). Thread: inference executor."""

    def __init__(self, package: ModelPackage) -> None:
        self.package = package
        self.product_id = package.product_id
        self.model_id: str | None = package.model_id
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2  # leave cores for capture, API and the event loop
        self._session = ort.InferenceSession(
            str(package.weights_path), sess_options=options, providers=["CPUExecutionProvider"]
        )
        self._input = self._session.get_inputs()[0].name
        # Warm up at load time so the first piece of a lot is not the slow one (~50 ms vs ~4 ms).
        size = package.preprocess.input_size
        self.classify_array(np.zeros((3, size, size), dtype=np.float32))

    def classify_array(self, array: np.ndarray) -> dict[Grade, float]:
        logits = self._session.run(None, {self._input: array[np.newaxis, ...]})[0][0]
        if logits.shape != (len(self.package.class_order),):
            raise ClassifierError(f"saída inesperada do modelo: {logits.shape}")
        probabilities = softmax(logits.astype(np.float64))
        return {g: float(p) for g, p in zip(self.package.class_order, probabilities, strict=True)}

    def classify(self, frame: Frame) -> Prediction:
        started = time.perf_counter()
        try:
            array = prepare_bytes(frame.data, self.package.preprocess)
        except OSError:
            # Unreadable image: not the model's call; the piece goes to review (INVALID_IMAGE).
            return Prediction(scores=None, latency_ms=(time.perf_counter() - started) * 1000)
        scores = self.classify_array(array)
        return Prediction(scores=scores, latency_ms=(time.perf_counter() - started) * 1000)
