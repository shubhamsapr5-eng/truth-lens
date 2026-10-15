"""
Unit Tests for Semantic Stance & NLI Classifier (65% Milestone)
"""

import pytest
from src.stance.stance_classifier import StanceClassifier, StanceType, StanceResult


@pytest.fixture(scope="module")
def classifier():
    return StanceClassifier(use_transformer=False)


def test_stance_supports(classifier):
    claim = "ISRO successfully landed Chandrayaan-3 on the lunar south pole"
    evidence = (
        "ISRO confirmed the historic achievement as Chandrayaan-3 successfully completed a soft landing "
        "near the lunar south pole on Wednesday."
    )
    res = classifier.classify_pair(claim, evidence)
    assert res.stance == StanceType.SUPPORTS
    assert res.phi_score == 1.0
    assert res.confidence >= 0.70
    assert res.support_prob > res.refute_prob


def test_stance_refutes(classifier):
    claim = "Drinking bleach is a proven miracle cure for viral infections"
    evidence = (
        "Health authorities debunked viral claims, calling the bleach treatment a dangerous hoax and false rumor "
        "with zero scientific evidence."
    )
    res = classifier.classify_pair(claim, evidence)
    assert res.stance == StanceType.REFUTES
    assert res.phi_score == -1.0
    assert res.confidence >= 0.70
    assert res.refute_prob > res.support_prob


def test_stance_neutral_unrelated(classifier):
    claim = "Federal Reserve raised benchmark interest rates by 25 basis points"
    evidence = (
        "Farmers in southern Spain reported a record harvest of organic citrus fruits following unseasonable rainfall."
    )
    res = classifier.classify_pair(claim, evidence)
    assert res.stance == StanceType.NEUTRAL
    assert res.phi_score == 0.0
    assert res.neutral_prob >= 0.60


def test_batch_classification(classifier):
    claim = "Scientists discovered evidence of liquid water beneath Martian surface"
    snippets = [
        "Planetary scientists confirmed radar observations indicating subglacial liquid water lakes on Mars.",
        "A critical study debunked the Martian water claim as a false instrument reflection artifact.",
        "Tokyo stock exchange ended Tuesday sessions slightly higher led by automotive shares."
    ]
    results = classifier.batch_classify(claim, snippets)
    assert len(results) == 3
    assert results[0].stance == StanceType.SUPPORTS
    assert results[1].stance == StanceType.REFUTES
    assert results[2].stance == StanceType.NEUTRAL
