"""
Unit and Integration Tests for TruthLens Phase 5 REST API Microservice
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "TruthLens News Credibility Engine" in data["service"]
    assert data["version"] == "1.0.0"
    assert len(data["endpoints"]) >= 4


def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mbfc_sources_indexed"] > 4000
    assert "ScoreAggregator" in data["modules_loaded"]


def test_api_sources_search():
    response = client.get("/api/sources/search?q=guardian")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("guardian" in item["domain"].lower() for item in data)


def test_api_reputation_known_high_trust():
    response = client.get("/api/reputation/reuters.com")
    assert response.status_code == 200
    data = response.json()
    assert data["domain"] == "reuters.com"
    assert data["percentage_score"] >= 80.0
    assert data["is_satire"] is False


def test_api_reputation_satire():
    response = client.get("/api/reputation/theonion.com")
    assert response.status_code == 200
    data = response.json()
    assert data["is_satire"] is True
    assert data["percentage_score"] == 0.0


def test_api_reputation_conspiracy():
    response = client.get("/api/reputation/naturalnews.com")
    assert response.status_code == 200
    data = response.json()
    assert data["is_conspiracy"] is True


def test_api_reputation_unknown_fallback():
    response = client.get("/api/reputation/nonexistent-journal-998877.com")
    assert response.status_code == 200
    data = response.json()
    assert data["is_fallback"] is True
    assert data["percentage_score"] == 50.0


def test_api_manipulation_clean():
    payload = {"text": "The lunar reconnaissance orbiter transmitted photographic data of the crater."}
    response = client.post("/api/manipulation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["manipulation_index"] < 25.0
    assert data["sensationalism_score"] < 20.0


def test_api_manipulation_sensational():
    payload = {"text": "SHOCKING BOMBSHELL: Big Pharma is hiding this one secret cure that doctors DON'T want you to know!!!"}
    response = client.post("/api/manipulation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["manipulation_index"] > 35.0
    assert len(data["flagged_phrases"]) > 0


def test_api_claims_extraction():
    payload = {"text": "ISRO landed Chandrayaan-3 on the lunar south pole in August 2023."}
    response = client.post("/api/claims", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["claims_count"] >= 1
    assert any("Chandrayaan" in c["text"] or "landed" in c["text"] for c in data["claims"])


def test_api_verify_endpoint_chandrayaan():
    payload = {
        "claim": "ISRO successfully completed a soft landing of Chandrayaan-3 on the lunar south pole",
        "origin_url": "https://www.reuters.com",
        "context_text": "ISRO confirmed the historic soft landing of Chandrayaan-3 on the lunar south pole on August 23, 2023."
    }
    response = client.post("/api/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["final_score"] >= 70.0
    assert "VERIFIED" in data["verdict"] or "CREDIBLE" in data["verdict"]
    assert "C_final" in data["formula_explanation"]
    assert data["evidence_articles_count"] > 0
    assert data["latency_ms"] > 0


def test_api_verify_satire_override():
    payload = {
        "claim": "Eating moon dust permanently halts all human aging",
        "origin_url": "https://theonion.com",
        "context_text": "Satirical report claims scientists discover miracle anti-aging dust."
    }
    response = client.post("/api/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["final_score"] == 0.0
    assert data["verdict"] == "SATIRE_PARODY"
