"""
Unit tests for NewsRetriever (Phase 3).
"""

import pytest
from src.retrieval.news_retriever import NewsRetriever, RetrievedArticle


def test_retriever_initialization():
    nr = NewsRetriever()
    assert nr is not None
    assert nr.db is not None


def test_retriever_fallback_evidence():
    nr = NewsRetriever(api_key="mock_invalid_key_for_test")
    articles = nr._get_fallback_evidence("economic inflation data", max_results=4)
    assert len(articles) == 4
    for a in articles:
        assert isinstance(a, RetrievedArticle)
        assert a.domain != ""
        assert a.credibility_score >= 0.0
        assert a.percentage_score >= 0.0
        assert a.weight_factor >= 0.0


def test_retriever_empty_query():
    nr = NewsRetriever()
    assert nr.search_evidence("") == []
    assert nr.search_evidence("   ") == []
