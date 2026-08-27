"""
Unit Tests for Source Reputation Database and Domain Resolver (Phase 2)
"""

import pytest
from src.database.source_reputation_db import SourceReputationDB
from src.utils.url_helper import extract_canonical_domain, extract_domain_parts, is_trusted_tld


@pytest.fixture(scope="module")
def rep_db():
    db = SourceReputationDB()
    yield db
    db.close()


def test_url_helper_canonical_extraction():
    assert extract_canonical_domain("https://edition.cnn.com/world") == "cnn.com"
    assert extract_canonical_domain("http://news.bbc.co.uk/story123") == "bbc.co.uk"
    assert extract_canonical_domain("www.thehindu.com") == "thehindu.com"
    assert extract_canonical_domain("https://sub.domain.isro.gov.in/test") == "isro.gov.in"
    assert extract_canonical_domain("reuters.com") == "reuters.com"


def test_trusted_tld_recognition():
    is_trusted, suffix, score = is_trusted_tld("https://cdc.gov/flu")
    assert is_trusted is True
    assert score >= 0.90

    is_trusted, suffix, score = is_trusted_tld("https://harvard.edu/research")
    assert is_trusted is True
    assert score >= 0.90

    is_trusted, suffix, score = is_trusted_tld("https://mysite.com")
    assert is_trusted is False


def test_high_credibility_sources(rep_db):
    reuters = rep_db.lookup("reuters.com")
    assert reuters.credibility_score >= 0.85
    assert reuters.factual_reporting in ["very high", "high"]
    assert reuters.is_satire is False

    bbc = rep_db.lookup("https://www.bbc.com/news")
    assert bbc.credibility_score >= 0.80

    hindu = rep_db.lookup("thehindu.com")
    assert hindu.credibility_score >= 0.80
    assert hindu.country == "india"


def test_satire_sources(rep_db):
    theonion = rep_db.lookup("theonion.com")
    assert theonion.is_satire is True
    assert theonion.credibility_score == 0.0
    assert theonion.weight_factor == 0.0

    babylonbee = rep_db.lookup("https://babylonbee.com/news/123")
    assert babylonbee.is_satire is True
    assert babylonbee.credibility_score == 0.0


def test_conspiracy_and_low_factuality_sources(rep_db):
    infowars = rep_db.lookup("infowars.com")
    assert infowars.is_conspiracy is True or infowars.credibility_score <= 0.20
    assert infowars.weight_factor <= 0.10


def test_subdomain_resolution(rep_db):
    rep_main = rep_db.lookup("cnn.com")
    rep_sub = rep_db.lookup("edition.cnn.com")
    assert rep_sub.domain == rep_main.domain
    assert rep_sub.credibility_score == rep_main.credibility_score


def test_unlisted_fallback(rep_db):
    unknown = rep_db.lookup("completely-unknown-fake-domain-999.xyz")
    assert unknown.is_fallback is True
    assert unknown.credibility_score == 0.50
    assert unknown.lookup_method == "unlisted_fallback"


def test_batch_lookup(rep_db):
    domains = [
        "reuters.com",
        "apnews.com",
        "theguardian.com",
        "nature.com",
        "infowars.com",
        "theonion.com",
        "livemint.com"
    ]
    results = rep_db.batch_lookup(domains)
    assert len(results) == len(domains)
    assert all(r.domain != "" for r in results)


def test_database_statistics(rep_db):
    stats = rep_db.get_statistics()
    assert stats["total_sources"] >= 4000
    assert "very high" in stats["factuality_distribution"] or "high" in stats["factuality_distribution"]
    assert stats["average_credibility_score"] > 0.0
