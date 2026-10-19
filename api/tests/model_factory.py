"""Builds a tiny but real ONNX model package for tests (no torch needed).

Graph: mean of each RGB channel -> linear layer -> 3 logits (A, B, C), so different simulated
drawings get different (meaningless) scores."""

import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

from amazonvision.vision.package import FORMAT_VERSION, sha256_file
from amazonvision.vision.preprocess import PreprocessSpec


def build_onnx(path: Path, size: int = 224) -> None:
    weight = np.array(
        [[0.8, -0.2, -0.6], [0.4, 0.1, -0.5], [-0.3, 0.2, 0.1]], dtype=np.float32
    )  # rows: R, G, B means; columns: A, B, C (small: no softmax saturation)
    bias = np.array([0.0, 0.5, 0.0], dtype=np.float32)
    graph = helper.make_graph(
        [
            helper.make_node("ReduceMean", ["image", "axes"], ["pooled"], keepdims=0),
            helper.make_node("MatMul", ["pooled", "weight"], ["mm"]),
            helper.make_node("Add", ["mm", "bias"], ["logits"]),
        ],
        "tiny",
        [helper.make_tensor_value_info("image", TensorProto.FLOAT, [1, 3, size, size])],
        [helper.make_tensor_value_info("logits", TensorProto.FLOAT, [1, 3])],
        initializer=[
            numpy_helper.from_array(np.array([2, 3], dtype=np.int64), "axes"),
            numpy_helper.from_array(weight, "weight"),
            numpy_helper.from_array(bias, "bias"),
        ],
    )
    model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 18)])
    model.ir_version = 9
    onnx.checker.check_model(model)
    onnx.save(model, str(path))


def build_package(
    root: Path,
    *,
    product_id: str = "tucuma",
    model_id: str | None = None,
    threshold: float | None = 0.6,
) -> Path:
    model_id = model_id or f"{product_id}-teste"
    folder = root / model_id
    folder.mkdir(parents=True, exist_ok=True)
    build_onnx(folder / "model.onnx")
    manifest = {
        "format_version": FORMAT_VERSION,
        "model_id": model_id,
        "product_id": product_id,
        "architecture": "tiny_test",
        "class_order": ["A", "B", "C"],
        "preprocess": PreprocessSpec().to_dict(),
        "dataset_version": "teste",
        "weights_sha256": sha256_file(folder / "model.onnx"),
        "recommended_threshold": threshold,
        "metrics": {"test_macro_f1": 0.9, "ready_for_bench": False},
        "created_at": datetime.now(UTC).isoformat(),
    }
    (folder / "model.json").write_text(json.dumps(manifest), "utf-8")
    (folder / "relatorio.md").write_text("# Relatório de teste\n", "utf-8")
    return folder
