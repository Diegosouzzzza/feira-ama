import pytest

from amazonvision.domain.quality import (
    AutoDecision,
    Destination,
    Grade,
    QualityPolicy,
    ReviewReason,
    decide,
)

POLICY = QualityPolicy(threshold=0.8)


def scores(a: float, b: float, c: float) -> dict[Grade, float]:
    return {Grade.A: a, Grade.B: b, Grade.C: c}


@pytest.mark.parametrize(
    ("values", "grade", "decision"),
    [
        ((0.90, 0.07, 0.03), Grade.A, AutoDecision.APPROVED),
        ((0.05, 0.85, 0.10), Grade.B, AutoDecision.REJECTED),
        ((0.02, 0.08, 0.90), Grade.C, AutoDecision.REJECTED),
        ((0.80, 0.15, 0.05), Grade.A, AutoDecision.APPROVED),
    ],
)
def test_confident_predictions_follow_destination_map(values, grade, decision):
    result = decide(scores(*values), POLICY)
    assert result.predicted_grade is grade
    assert result.decision is decision
    assert result.review_reason is None
    assert result.confidence == max(values)


def test_low_confidence_goes_to_review_but_keeps_prediction():
    result = decide(scores(0.6, 0.3, 0.1), POLICY)
    assert result.decision is AutoDecision.REVIEW
    assert result.review_reason is ReviewReason.LOW_CONFIDENCE
    assert result.predicted_grade is Grade.A
    assert result.confidence == 0.6


def test_inconclusive_is_never_recorded_as_grade_c():
    result = decide(scores(0.34, 0.33, 0.33), POLICY)
    assert result.decision is AutoDecision.REVIEW
    assert result.predicted_grade is Grade.A


def test_tie_at_the_top_is_ambiguous_even_with_low_threshold():
    result = decide(scores(0.5, 0.5, 0.0), QualityPolicy(threshold=0.1))
    assert result.decision is AutoDecision.REVIEW
    assert result.review_reason is ReviewReason.AMBIGUOUS


def test_invalid_image_goes_to_review_without_prediction():
    result = decide(None, POLICY)
    assert result.decision is AutoDecision.REVIEW
    assert result.review_reason is ReviewReason.INVALID_IMAGE
    assert result.predicted_grade is None
    assert result.confidence is None


def test_custom_destination_map():
    policy = QualityPolicy(
        threshold=0.5,
        destinations={
            Grade.A: Destination.APPROVED,
            Grade.B: Destination.APPROVED,
            Grade.C: Destination.REJECTED,
        },
    )
    assert decide(scores(0.1, 0.8, 0.1), policy).decision is AutoDecision.APPROVED


@pytest.mark.parametrize(
    "bad",
    [
        {Grade.A: 0.5, Grade.B: 0.5},
        scores(0.5, 0.5, 0.5),
        scores(1.2, -0.1, -0.1),
        scores(float("nan"), 0.5, 0.5),
    ],
)
def test_malformed_scores_are_rejected(bad):
    with pytest.raises(ValueError):
        decide(bad, POLICY)


@pytest.mark.parametrize("threshold", [0.0, -0.1, 1.01])
def test_threshold_must_be_in_range(threshold):
    with pytest.raises(ValueError):
        QualityPolicy(threshold=threshold)


def test_destinations_must_cover_all_grades():
    with pytest.raises(ValueError):
        QualityPolicy(threshold=0.5, destinations={Grade.A: Destination.APPROVED})
