"""Evaluation of a classifier through the real decision policy.

Model accuracy (argmax) and operational outcomes (what the bench would do with the threshold) are
reported separately: a correct class with a low score still goes to review."""

from collections.abc import Sequence
from typing import Any

from amazonvision.domain.quality import AutoDecision, Grade, QualityPolicy, decide

ORDER = (Grade.A, Grade.B, Grade.C)
DEFECTIVE = (Grade.B, Grade.C)


def _ratio(num: int, den: int) -> float | None:
    return num / den if den else None


def classification_metrics(
    y_true: Sequence[Grade], scores: Sequence[dict[Grade, float]]
) -> dict[str, Any]:
    predicted = [max(s, key=lambda g: s[g]) for s in scores]
    index = {g: i for i, g in enumerate(ORDER)}
    confusion = [[0, 0, 0] for _ in ORDER]
    for t, p in zip(y_true, predicted, strict=True):
        confusion[index[t]][index[p]] += 1
    per_class: dict[str, dict[str, float | int | None]] = {}
    f1s = []
    for g in ORDER:
        i = index[g]
        tp = confusion[i][i]
        support = sum(confusion[i])
        predicted_as = sum(row[i] for row in confusion)
        precision = _ratio(tp, predicted_as)
        recall = _ratio(tp, support)
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision is not None and recall is not None and precision + recall > 0
            else 0.0
        )
        f1s.append(f1)
        per_class[g.value] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
        }
    accuracy = _ratio(sum(confusion[i][i] for i in range(3)), len(y_true))
    return {
        "n": len(y_true),
        "class_order": [g.value for g in ORDER],
        "confusion": confusion,
        "per_class": per_class,
        "macro_f1": sum(f1s) / len(f1s),
        "accuracy": accuracy,
    }


def policy_metrics(
    y_true: Sequence[Grade], scores: Sequence[dict[Grade, float]], threshold: float
) -> dict[str, Any]:
    policy = QualityPolicy(threshold=threshold)
    decisions = [decide(s, policy).decision for s in scores]
    defective = [d for t, d in zip(y_true, decisions, strict=True) if t in DEFECTIVE]
    good = [d for t, d in zip(y_true, decisions, strict=True) if t is Grade.A]
    review = sum(d is AutoDecision.REVIEW for d in decisions)
    false_approvals = sum(d is AutoDecision.APPROVED for d in defective)
    defect_rejected = sum(d is AutoDecision.REJECTED for d in defective)
    good_rejected = sum(d is AutoDecision.REJECTED for d in good)
    return {
        "threshold": threshold,
        "n": len(decisions),
        "automatic_coverage": _ratio(len(decisions) - review, len(decisions)),
        "review_rate": _ratio(review, len(decisions)),
        "defective_total": len(defective),
        "defective_rejected_rate": _ratio(defect_rejected, len(defective)),
        "defective_false_approval_rate": _ratio(false_approvals, len(defective)),
        "defective_false_approvals": false_approvals,
        "good_total": len(good),
        "good_wrongly_rejected_rate": _ratio(good_rejected, len(good)),
    }


def choose_threshold(
    y_true: Sequence[Grade],
    scores: Sequence[dict[Grade, float]],
    *,
    max_false_approval: float = 0.05,
) -> tuple[float, dict[str, Any]]:
    """Lowest threshold (most automatic decisions) keeping B/C false approvals within target.

    Chosen on validation data only, then frozen before looking at the test set."""
    candidates = [round(0.40 + 0.01 * i, 2) for i in range(60)]  # 0.40 .. 0.99
    for threshold in candidates:
        metrics = policy_metrics(y_true, scores, threshold)
        rate = metrics["defective_false_approval_rate"]
        if rate is None or rate <= max_false_approval:
            return threshold, {**metrics, "target_met": True}
    return 0.99, {**policy_metrics(y_true, scores, 0.99), "target_met": False}
