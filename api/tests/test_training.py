from pathlib import Path

import pytest

from amazonvision.domain.quality import Grade
from amazonvision.training.dataset import (
    Sample,
    check_no_leakage,
    read_manifest,
    split_by_physical_sample,
)
from amazonvision.training.evaluate import (
    choose_threshold,
    classification_metrics,
    policy_metrics,
)


def samples(pieces: int, photos: int) -> list[Sample]:
    return [
        Sample(f"{g.value}-{p}-{f}.png", "tucuma", f"{g.value}-{p}", g)
        for g in Grade
        for p in range(pieces)
        for f in range(photos)
    ]


def test_split_keeps_each_piece_in_one_partition_and_covers_every_class():
    result = split_by_physical_sample(samples(10, 4))
    check_no_leakage(result)
    for split in ("train", "val", "test"):
        labels = {s.label for s in result if s.split == split}
        assert labels == set(Grade), split


def test_split_rejects_piece_with_two_labels():
    bad = [Sample("1.png", "tucuma", "P1", Grade.A), Sample("2.png", "tucuma", "P1", Grade.B)]
    with pytest.raises(ValueError, match="rótulos diferentes"):
        split_by_physical_sample(bad)


def test_leakage_is_detected():
    leaked = [
        Sample("1.png", "t", "P1", Grade.A, "train"),
        Sample("2.png", "t", "P1", Grade.A, "test"),
    ]
    with pytest.raises(ValueError, match="mais de uma partição"):
        check_no_leakage(leaked)


def scores(a: float, b: float, c: float) -> dict[Grade, float]:
    return {Grade.A: a, Grade.B: b, Grade.C: c}


def test_metrics_count_false_approvals_of_defective_pieces():
    y = [Grade.A, Grade.B, Grade.C, Grade.B]
    s = [
        scores(0.9, 0.05, 0.05),
        scores(0.85, 0.1, 0.05),
        scores(0.1, 0.1, 0.8),
        scores(0.5, 0.45, 0.05),
    ]
    m = classification_metrics(y, s)
    assert m["confusion"] == [[1, 0, 0], [2, 0, 0], [0, 0, 1]]
    p = policy_metrics(y, s, 0.8)
    assert p["defective_false_approvals"] == 1
    assert p["defective_false_approval_rate"] == pytest.approx(1 / 3)
    assert p["review_rate"] == pytest.approx(1 / 4)


def test_threshold_is_the_lowest_meeting_the_target():
    y = [Grade.A, Grade.B]
    s = [scores(0.95, 0.03, 0.02), scores(0.7, 0.2, 0.1)]
    threshold, info = choose_threshold(y, s, max_false_approval=0.0)
    assert threshold == pytest.approx(0.71)
    assert info["target_met"] is True


def test_full_training_produces_a_loadable_package(tmp_path: Path):
    pytest.importorskip("torch", reason="grupo de dependências 'training' não instalado")
    from amazonvision.training.synthetic import generate
    from amazonvision.training.train import train
    from amazonvision.vision.package import load_package

    manifest = generate(
        tmp_path / "ds", product_id="tucuma", pieces_per_class=6, photos_per_piece=2
    )
    package_dir = train(
        manifest, product_id="tucuma", out_dir=tmp_path / "out", epochs=1, pretrained=False
    )
    package = load_package(package_dir)
    assert package.product_id == "tucuma"
    assert package.recommended_threshold is not None
    assert "ready_for_bench" in package.metrics
    report = (package_dir / "relatorio.md").read_text(encoding="utf-8")
    assert "## Parecer" in report
    check_no_leakage(read_manifest(package_dir / "dataset_split.csv"))


def test_training_bakes_the_roi_into_the_package(tmp_path: Path):
    pytest.importorskip("torch", reason="grupo de dependências 'training' não instalado")
    from amazonvision.training.synthetic import generate
    from amazonvision.training.train import train
    from amazonvision.vision.package import load_package
    from amazonvision.vision.preprocess import RoiSpec

    manifest = generate(
        tmp_path / "ds", product_id="tucuma", pieces_per_class=6, photos_per_piece=2
    )
    roi = RoiSpec(x=0.2, y=0.1, width=0.6, height=0.8)
    package_dir = train(
        manifest,
        product_id="tucuma",
        out_dir=tmp_path / "out",
        epochs=1,
        pretrained=False,
        roi=roi,
    )
    package = load_package(package_dir)
    assert package.preprocess.roi == roi
