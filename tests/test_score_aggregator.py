"""
Unit Tests for Unified Mathematical Score Aggregator (65% Milestone)
"""

import pytest
from src.scoring.score_aggregator import ScoreAggregator, VerdictTier
from src.stance.stance_classifier import StanceResult, StanceType
from src.retrieval.news_retriever import RetrievedArticle
from src.manipulation.manipulation_detector import ManipulationReport


@pytest.fixture(scope="module")
def aggregator():
    return ScoreAggregator()


def make_dummy_article(name: str, domain: str, score: float = 0.85, weight: float = 0.85):
    return RetrievedArticle(
        title=f"Report by {name}",
        source_name=name,
        url=f"https://{domain}/article",
        domain=domain,
        snippet="Official investigation details.",
        published_at="2026-10-15",
        credibility_score=score,
        percentage_score=score * 100.0,
        weight_factor=weight
    )


def test_score_aggregator_verified_case(aggregator):
    # Origin: High trust (e.g. Reuters = 90.0)
    origin_score = 90.0
    articles = [
        make_dummy_article("Reuters", "reuters.com", 0.90, 0.90),
        make_dummy_article("BBC", "bbc.co.uk", 0.85, 0.85),
    ]
    stances = [
        StanceResult(claim="c", evidence="e", stance=StanceType.SUPPORTS, phi_score=1.0, confidence=0.9),
        StanceResult(claim="c", evidence="e", stance=StanceType.SUPPORTS, phi_score=1.0, confidence=0.85),
    ]
    # Minimal manipulation (M = 4.0)
    manip = ManipulationReport(overall_manipulation_score=4.0)

    assessment = aggregator.aggregate(origin_score, articles, stances, manip)

    assert assessment.verdict == VerdictTier.VERIFIED_CREDIBLE
    assert assessment.final_score >= 80.0
    assert assessment.supporting_sources_count == 2
    assert assessment.evidence_score >= 85.0
    assert "0.70" in assessment.math_formula_explanation


def test_score_aggregator_refuted_case(aggregator):
    origin_score = 50.0  # unknown or low source
    articles = [
        make_dummy_article("AP News", "apnews.com", 0.90, 0.90),
        make_dummy_article("Reuters", "reuters.com", 0.90, 0.90),
    ]
    stances = [
        StanceResult(claim="c", evidence="e", stance=StanceType.REFUTES, phi_score=-1.0, confidence=0.9),
        StanceResult(claim="c", evidence="e", stance=StanceType.REFUTES, phi_score=-1.0, confidence=0.85),
    ]
    manip = ManipulationReport(overall_manipulation_score=10.0)

    assessment = aggregator.aggregate(origin_score, articles, stances, manip)

    assert assessment.verdict == VerdictTier.LOW_CREDIBILITY
    assert assessment.final_score <= 35.0
    assert assessment.refuting_sources_count == 2
    assert assessment.evidence_score <= 20.0


def test_score_aggregator_satire_override(aggregator):
    articles = [make_dummy_article("Reuters", "reuters.com", 0.90, 0.90)]
    stances = [StanceResult(claim="c", evidence="e", stance=StanceType.NEUTRAL, phi_score=0.0)]
    manip = ManipulationReport(overall_manipulation_score=0.0)

    assessment = aggregator.aggregate(0.0, articles, stances, manip, is_satire=True)
    assert assessment.verdict == VerdictTier.SATIRE_PARODY
    assert assessment.final_score == 0.0


def test_score_aggregator_manipulation_penalty(aggregator):
    # Comparing score before and after manipulation penalty
    articles = [make_dummy_article("BBC", "bbc.co.uk", 0.85, 0.85)]
    stances = [StanceResult(claim="c", evidence="e", stance=StanceType.SUPPORTS, phi_score=1.0, confidence=0.8)]
    
    clean_manip = ManipulationReport(overall_manipulation_score=0.0)
    heavy_manip = ManipulationReport(overall_manipulation_score=80.0)

    clean_res = aggregator.aggregate(85.0, articles, stances, clean_manip)
    dirty_res = aggregator.aggregate(85.0, articles, stances, heavy_manip)

    # 80.0 * 0.25 = 20.0 points penalty
    assert dirty_res.manipulation_penalty == 20.0
    assert dirty_res.final_score < clean_res.final_score
