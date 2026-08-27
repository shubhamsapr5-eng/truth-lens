"""
Unit Tests for Manipulation & Sensationalism Detection Engine (Phase 2)
"""

import pytest
from src.manipulation.manipulation_detector import ManipulationDetector


@pytest.fixture(scope="module")
def detector():
    return ManipulationDetector()


def test_clean_journalistic_text(detector):
    headline = "Federal Reserve keeps interest rate unchanged amid cooling inflation"
    body = "The central bank decided to hold policy rates in the current target range as quarterly economic figures aligned with expectations."
    report = detector.analyze(headline=headline, body=body)

    assert report.overall_manipulation_score < 20.0
    assert report.risk_level in ["Low / Standard Journalistic", "Mild Sensationalism"]
    assert len(report.flagged_phrases) == 0


def test_sensationalist_clickbait_headline(detector):
    headline = "SHOCKING BOMBSHELL: You Won't Believe What Leaked Documents Reveal!!!"
    body = "Terrifying new secrets exposed! Mainstream media won't tell you the truth. Act now before it is too late!"
    report = detector.analyze(headline=headline, body=body)

    assert report.overall_manipulation_score >= 50.0
    assert report.sensationalism_score > 0
    assert report.fear_urgency_score > 0
    assert len(report.flagged_phrases) > 0
    assert len(report.stylistic_flags) > 0


def test_conspiracy_and_pseudoscience_markers(detector):
    headline = "Deep state cabal plandemic exposed: Doctors are baffled by miracle cure big pharma is hiding"
    report = detector.analyze(headline=headline)

    assert report.conspiracy_score > 0
    assert report.pseudoscience_score > 0
    assert report.overall_manipulation_score > 30.0


def test_stylistic_markers_only(detector):
    headline = "UNPRECEDENTED DISASTER INCOMING???!!!"
    report = detector.analyze(headline=headline)

    assert report.stylistic_score > 0
    assert any("Excessive punctuation" in f for f in report.stylistic_flags)
