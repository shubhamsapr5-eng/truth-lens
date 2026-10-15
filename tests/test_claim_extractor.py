"""
Unit Tests for Factual Claim Extraction (65% Milestone)
"""

import pytest
from src.claim_extraction.claim_extractor import ClaimExtractor, ExtractedClaim


@pytest.fixture(scope="module")
def extractor():
    return ClaimExtractor(use_spacy=True)


def test_claim_extraction_from_factual_news(extractor):
    article = (
        "ISRO successfully launched the Chandrayaan-3 spacecraft on July 14, 2023, from Sriharikota. "
        "The mission successfully completed a soft landing on the lunar South Pole on August 23, 2023. "
        "In my opinion, space exploration is very exciting and fun. "
        "What do you think about the future of moon exploration?"
    )

    claims = extractor.extract_claims(article, max_claims=3)
    assert len(claims) >= 2

    # Verify primary claim has high salience
    primary = claims[0]
    assert primary.is_primary is True
    assert primary.salience_score >= 0.70
    assert any("Chandrayaan" in c.text or "ISRO" in c.text for c in claims)

    # Verify questions and opinions are filtered out
    texts = [c.text for c in claims]
    assert not any("What do you think" in t for t in texts)
    assert not any("In my opinion" in t for t in texts)


def test_claim_entity_and_numerical_detection(extractor):
    sentence = "The Federal Reserve raised interest rates by 25 basis points to 5.5% on Wednesday in Washington."
    claims = extractor.extract_claims(sentence)
    assert len(claims) == 1
    c = claims[0]
    assert c.has_numbers is True
    assert c.salience_score >= 0.70
    assert len(c.entities) >= 1


def test_empty_or_trivial_input(extractor):
    assert extractor.extract_claims("") == []
    assert extractor.extract_claims("   ") == []
    assert extractor.extract_claims("Hello. Yes. Bye.") == []
