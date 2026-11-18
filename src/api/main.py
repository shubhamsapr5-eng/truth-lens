"""
TruthLens Phase 5 - FastAPI Production Microservice
Exposes RESTful endpoints for real-time news credibility assessment,
outlet reputation queries, claim extraction, and sensationalism analysis.
"""

import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.database.source_reputation_db import SourceReputationDB
from src.database.schema import SourceReputation
from src.manipulation.manipulation_detector import ManipulationDetector, ManipulationReport
from src.claim_extraction.claim_extractor import ClaimExtractor
from src.retrieval.news_retriever import NewsRetriever, RetrievedArticle
from src.stance.stance_classifier import StanceClassifier, StanceResult
from src.scoring.score_aggregator import ScoreAggregator, CredibilityAssessment

# Initialize FastAPI application
app = FastAPI(
    title="TruthLens Real-Time News Credibility API",
    description=(
        "Production AI-Powered REST API for news credibility, source reputation, "
        "and disinformation detection. PSAIAC_61 Final Review Milestone."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin access (e.g. from localsort.in frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service singletons
db = SourceReputationDB()
manipulation_detector = ManipulationDetector()
claim_extractor = ClaimExtractor()
news_retriever = NewsRetriever()
stance_classifier = StanceClassifier()
score_aggregator = ScoreAggregator()


# ==============================================================================
# Request & Response Schemas
# ==============================================================================

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "TruthLens Verification Engine"
    version: str = "1.0.0"
    mbfc_sources_indexed: int
    modules_loaded: List[str]


class ManipulationRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Article text or headline to analyze")


class ClaimsRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Full article or statement to extract claims from")


class VerifyRequest(BaseModel):
    claim: str = Field(..., min_length=3, description="Factual claim to verify")
    origin_url: Optional[str] = Field(None, description="Origin domain or article URL")
    context_text: Optional[str] = Field(None, description="Surrounding article paragraph or text")


class StanceDetail(BaseModel):
    source: str
    domain: str
    title: str
    stance: str
    confidence: float
    reputation_weight: float
    is_satire: bool
    is_conspiracy: bool


class VerificationResponse(BaseModel):
    claim: str
    final_score: float
    verdict: str
    verdict_badge: str
    summary_verdict: str
    evidence_score: float
    origin_score: float
    manipulation_index: float
    manipulation_penalty: float
    formula_explanation: str
    origin_reputation: Dict[str, Any]
    manipulation_report: Dict[str, Any]
    evidence_articles_count: int
    stances: List[StanceDetail]
    key_findings: List[str]
    latency_ms: float


# ==============================================================================
# API Endpoints
# ==============================================================================

@app.get("/", tags=["System"])
def root():
    """Service metadata and routing overview."""
    return {
        "service": "TruthLens News Credibility Engine",
        "milestone": "Phase 5 - 100% Final Review Release",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": [
            "/health",
            "/api/reputation/{domain}",
            "/api/manipulation",
            "/api/claims",
            "/api/verify"
        ]
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Verify backend health and database readiness."""
    stats = db.get_statistics()
    count = stats.get("total_sources", 0)
    return HealthResponse(
        status="ok",
        service="TruthLens Verification Engine",
        version="1.0.0",
        mbfc_sources_indexed=count,
        modules_loaded=[
            "SourceReputationDB",
            "ManipulationDetector",
            "ClaimExtractor",
            "NewsRetriever",
            "StanceClassifier",
            "ScoreAggregator"
        ]
    )


@app.get("/api/sources/search", tags=["Reputation"])
def search_sources(
    q: str = Query(..., min_length=1, description="Domain substring or outlet name query"),
    limit: int = Query(25, ge=1, le=100)
):
    """
    Search across all 4,442 MBFC indexed sources by fuzzy substring matching
    on domain or publication name.
    """
    results = db.search_domains(q, limit=limit)
    return [
        {
            "domain": r.domain,
            "source_name": r.source_name,
            "bias": r.bias,
            "factual_reporting": r.factual_reporting,
            "credibility_score": r.credibility_score,
            "percentage_score": r.percentage_score,
            "is_satire": r.is_satire,
            "is_conspiracy": r.is_conspiracy,
            "is_fallback": r.is_fallback,
            "country": r.country,
            "notes": r.notes
        }
        for r in results
    ]


@app.get("/api/reputation/{domain:path}", tags=["Reputation"])
def get_reputation(domain: str):
    """
    Look up source reputation, factuality rating, and bias for any domain or URL.
    Returns authoritative data from the MBFC 4,400+ database or heuristic fallback.
    """
    if not domain or not domain.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Domain or URL parameter cannot be empty."
        )

    clean_domain = domain.strip().lower()
    rep: SourceReputation = db.lookup(clean_domain)
    
    return {
        "domain": rep.domain,
        "source_name": rep.source_name,
        "bias": rep.bias,
        "factual_reporting": rep.factual_reporting,
        "credibility_score": rep.credibility_score,
        "percentage_score": rep.percentage_score,
        "is_satire": rep.is_satire,
        "is_conspiracy": rep.is_conspiracy,
        "is_fallback": rep.is_fallback,
        "country": rep.country,
        "notes": rep.notes
    }


@app.post("/api/manipulation", tags=["Manipulation"])
def analyze_manipulation(request: ManipulationRequest):
    """
    Analyze text for linguistic manipulation, clickbait triggers,
    and sensationalism.
    """
    report = manipulation_detector.analyze(request.text)
    return {
        "manipulation_index": report.overall_manipulation_score,
        "sensationalism_score": report.sensationalism_score,
        "fear_urgency_score": report.fear_urgency_score,
        "conspiracy_score": report.conspiracy_score,
        "pseudoscience_score": report.pseudoscience_score,
        "stylistic_score": report.stylistic_score,
        "risk_level": report.risk_level,
        "flagged_phrases": report.flagged_phrases,
        "summary": report.summary_warning
    }


@app.post("/api/claims", tags=["Claim Extraction"])
def extract_claims(request: ClaimsRequest):
    """
    Extract check-worthy factual claims from raw input text.
    """
    claims = claim_extractor.extract_claims(request.text)
    return {
        "text_length": len(request.text),
        "claims_count": len(claims),
        "claims": [
            {
                "claim_id": c.claim_id,
                "text": c.text,
                "salience_score": c.salience_score,
                "entities": c.entities,
                "reasoning": c.reasoning,
                "is_primary": c.is_primary
            }
            for c in claims
        ]
    }


@app.post("/api/verify", response_model=VerificationResponse, tags=["Verification"])
def verify_claim(request: VerifyRequest):
    """
    Execute complete end-to-end multi-source credibility verification pipeline.
    Combines publisher reputation, stance consensus, and manipulation penalties.
    """
    t_start = time.perf_counter()

    claim = request.claim.strip()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Claim string cannot be blank."
        )

    # 1. Source Reputation
    origin_domain = request.origin_url or "https://www.unknown-source.com"
    origin_rep = db.lookup(origin_domain)

    # 2. Manipulation Detection
    text_to_analyze = request.context_text if request.context_text else claim
    manip_report = manipulation_detector.analyze(text_to_analyze)

    # 3. Evidence Retrieval
    articles = news_retriever.search_evidence(claim, max_results=5)

    # 4. Stance Classification
    stances = []
    stance_details = []
    for art in articles:
        ev_text = f"{art.title}. {art.snippet}"
        st_res = stance_classifier.classify_pair(claim, ev_text)
        stances.append(st_res)

        art_rep = db.lookup(art.domain)
        stance_details.append(StanceDetail(
            source=art.source_name,
            domain=art.domain,
            title=art.title,
            stance=st_res.stance.value,
            confidence=st_res.confidence,
            reputation_weight=art_rep.percentage_score,
            is_satire=art_rep.is_satire,
            is_conspiracy=art_rep.is_conspiracy
        ))

    # 5. Algebraic Credibility Aggregation
    assessment = score_aggregator.aggregate(
        origin_score=origin_rep.percentage_score,
        articles=articles,
        stances=stances,
        manipulation_report=manip_report,
        is_satire=origin_rep.is_satire,
        is_conspiracy=origin_rep.is_conspiracy
    )

    t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    return VerificationResponse(
        claim=claim,
        final_score=round(assessment.final_score, 1),
        verdict=assessment.verdict.value,
        verdict_badge=assessment.verdict_badge,
        summary_verdict=assessment.summary_verdict,
        evidence_score=round(assessment.evidence_score, 1),
        origin_score=round(assessment.origin_score, 1),
        manipulation_index=round(assessment.manipulation_index, 1),
        manipulation_penalty=round(assessment.manipulation_penalty, 1),
        formula_explanation=assessment.math_formula_explanation,
        origin_reputation={
            "domain": origin_rep.domain,
            "source_name": origin_rep.source_name,
            "factual_reporting": origin_rep.factual_reporting,
            "percentage_score": origin_rep.percentage_score,
            "is_satire": origin_rep.is_satire,
            "is_conspiracy": origin_rep.is_conspiracy,
        },
        manipulation_report={
            "manipulation_index": round(manip_report.overall_manipulation_score, 1),
            "sensationalism_score": round(manip_report.sensationalism_score, 1),
            "fear_urgency_score": round(manip_report.fear_urgency_score, 1),
            "flagged_phrases": manip_report.flagged_phrases
        },
        evidence_articles_count=len(articles),
        stances=stance_details,
        key_findings=assessment.key_findings,
        latency_ms=round(t_elapsed_ms, 2)
    )
