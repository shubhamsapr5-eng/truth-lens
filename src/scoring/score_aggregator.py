"""
Unified Mathematical Credibility Score Aggregator for TruthLens (65% Milestone)

Implements the formal peer-reviewed scoring equation:
  C_final = 0.70 * S_evidence + 0.30 * W_origin - (0.25 * M_index)

Where:
  • S_evidence: Multi-source weighted consensus score derived from NLI stance (Phi)
                and source reputation weights (W_rep) across independent reporting outlets.
  • W_origin:   Baseline credibility percentage (0-100) of the originating publisher domain.
  • M_index:    Linguistic manipulation, sensationalism, and clickbait score (0-100).
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from src.stance.stance_classifier import StanceResult, StanceType
from src.retrieval.news_retriever import RetrievedArticle
from src.manipulation.manipulation_detector import ManipulationReport


class VerdictTier(str, Enum):
    VERIFIED_CREDIBLE = "VERIFIED_CREDIBLE"
    LIKELY_CREDIBLE = "LIKELY_CREDIBLE"
    CONTESTED_OR_MIXED = "CONTESTED_OR_MIXED"
    LOW_CREDIBILITY = "LOW_CREDIBILITY"
    MANIPULATED_OR_MISLEADING = "MANIPULATED_OR_MISLEADING"
    SATIRE_PARODY = "SATIRE_PARODY"
    CONSPIRACY_PSEUDOSCIENCE = "CONSPIRACY_PSEUDOSCIENCE"


class CredibilityAssessment(BaseModel):
    """Complete mathematical assessment of news credibility."""
    final_score: float = Field(default=50.0, ge=0.0, le=100.0)
    verdict: VerdictTier
    verdict_badge: str = ""
    summary_verdict: str = ""
    
    # Mathematical Components
    evidence_score: float = Field(default=50.0, ge=0.0, le=100.0)      # S_evidence
    origin_score: float = Field(default=50.0, ge=0.0, le=100.0)        # W_origin
    manipulation_index: float = Field(default=0.0, ge=0.0, le=100.0)   # M_index
    manipulation_penalty: float = Field(default=0.0, ge=0.0, le=25.0)  # 0.25 * M_index
    
    # Evidence Pool Metrics
    total_evidence_sources: int = 0
    supporting_sources_count: int = 0
    refuting_sources_count: int = 0
    neutral_sources_count: int = 0
    weighted_consensus_phi: float = 0.0  # -1.0 to +1.0
    
    # Transparent Audit Trail
    math_formula_explanation: str = ""
    key_findings: List[str] = Field(default_factory=list)


class ScoreAggregator:
    """
    Computes unified credibility scores by synthesizing multi-source stance consensus,
    publisher authority weights, and lexical manipulation metrics.
    """

    def __init__(
        self,
        weight_evidence: float = 0.70,
        weight_origin: float = 0.30,
        manipulation_factor: float = 0.25
    ):
        self.w_evidence = weight_evidence
        self.w_origin = weight_origin
        self.m_factor = manipulation_factor

    def compute_evidence_consensus(
        self,
        articles: List[RetrievedArticle],
        stances: List[StanceResult]
    ) -> Dict[str, Any]:
        """
        Calculates S_evidence from article weights (W_rep) and NLI stances (Phi).
        Formula:
          Phi_bar = sum(W_rep_i * Phi_i * Conf_i) / sum(W_rep_i)
          S_evidence = (Phi_bar + 1.0) * 50.0  -> maps [-1.0, 1.0] to [0.0, 100.0]
        """
        if not articles or not stances:
            return {
                "s_evidence": 50.0,
                "phi_bar": 0.0,
                "supports": 0,
                "refutes": 0,
                "neutral": 0,
                "total": 0
            }

        n = min(len(articles), len(stances))
        weighted_sum = 0.0
        weight_total = 0.0
        sup_cnt = 0
        ref_cnt = 0
        neu_cnt = 0

        for i in range(n):
            art = articles[i]
            st = stances[i]

            w_rep = max(0.1, art.weight_factor)
            phi = st.phi_score
            conf = st.confidence

            # Track counts
            if st.stance == StanceType.SUPPORTS:
                sup_cnt += 1
            elif st.stance == StanceType.REFUTES:
                ref_cnt += 1
            else:
                neu_cnt += 1

            # Weighted stance impact
            weighted_sum += (w_rep * phi * conf)
            weight_total += w_rep

        if weight_total > 0:
            phi_bar = weighted_sum / weight_total
        else:
            phi_bar = 0.0

        # Clamp phi_bar to [-1.0, 1.0]
        phi_bar = max(-1.0, min(1.0, phi_bar))

        # Map to percentage scale [0.0, 100.0]
        s_evidence = round((phi_bar + 1.0) * 50.0, 1)

        return {
            "s_evidence": s_evidence,
            "phi_bar": round(phi_bar, 3),
            "supports": sup_cnt,
            "refutes": ref_cnt,
            "neutral": neu_cnt,
            "total": n
        }

    def aggregate(
        self,
        origin_score: float,
        articles: List[RetrievedArticle],
        stances: List[StanceResult],
        manipulation_report: Optional[ManipulationReport] = None,
        is_satire: bool = False,
        is_conspiracy: bool = False
    ) -> CredibilityAssessment:
        """
        Aggregates all components into a final credibility assessment.
        """
        # 1. Compute Evidence Consensus (S_evidence)
        ev_metrics = self.compute_evidence_consensus(articles, stances)
        s_evidence = ev_metrics["s_evidence"]
        phi_bar = ev_metrics["phi_bar"]

        # 2. Origin score (W_origin)
        w_origin = max(0.0, min(100.0, origin_score))

        # 3. Manipulation score (M_index)
        m_index = manipulation_report.overall_manipulation_score if manipulation_report else 0.0
        m_penalty = round(self.m_factor * m_index, 2)

        # 4. Raw Unified Credibility Score
        raw_final = (self.w_evidence * s_evidence) + (self.w_origin * w_origin) - m_penalty
        final_score = round(max(0.0, min(100.0, raw_final)), 1)

        # 5. Overrides & Verdict Classification
        key_findings = []

        if is_satire:
            final_score = 0.0
            verdict = VerdictTier.SATIRE_PARODY
            verdict_badge = "🎭 SATIRE / PARODY"
            summary_verdict = "Originates from a recognized satirical humor outlet. Not factual news."
            key_findings.append("Publisher domain is cataloged as 100% satirical entertainment.")
        elif is_conspiracy:
            final_score = min(final_score, 15.0)
            verdict = VerdictTier.CONSPIRACY_PSEUDOSCIENCE
            verdict_badge = "⚠️ CONSPIRACY / PSEUDOSCIENCE"
            summary_verdict = "Originates from an outlet with recorded history of conspiracy theories."
            key_findings.append("Source has documented track record of promoting debunked conspiracy narratives.")
        elif ev_metrics["refutes"] > 0 and ev_metrics["refutes"] >= ev_metrics["supports"]:
            if final_score > 35.0:
                final_score = 25.0  # Cap score if independent consensus refutes
            verdict = VerdictTier.LOW_CREDIBILITY
            verdict_badge = "🔴 DEBUNKED / REFUTED"
            summary_verdict = "Refuted by independent press consensus and fact-checking records."
            key_findings.append(f"{ev_metrics['refutes']} independent news sources explicitly refute the claim.")
        elif m_index >= 55.0:
            verdict = VerdictTier.MANIPULATED_OR_MISLEADING
            verdict_badge = "⚠️ MANIPULATED NARRATIVE"
            summary_verdict = "Severe linguistic manipulation and emotional panic triggers detected."
            key_findings.append(f"High manipulation index ({m_index:.1f}/100) penalties applied (-{m_penalty:.1f} pts).")
        elif final_score >= 75.0:
            verdict = VerdictTier.VERIFIED_CREDIBLE
            verdict_badge = "🟢 HIGH CREDIBILITY (VERIFIED)"
            summary_verdict = "Strong corroboration from high-reputation independent news outlets with factual tone."
            key_findings.append(f"Corroborated by {ev_metrics['supports']} reputable reporting sources.")
            key_findings.append(f"Source publisher authority rating: {w_origin:.0f}%.")
        elif final_score >= 50.0:
            verdict = VerdictTier.LIKELY_CREDIBLE
            verdict_badge = "🟡 MODERATE / LIKELY CREDIBLE"
            summary_verdict = "Generally supported by news evidence, with moderate corroboration."
            key_findings.append("Evidence pool shows positive alignment with minor variance.")
        else:
            verdict = VerdictTier.CONTESTED_OR_MIXED
            verdict_badge = "🟠 CONTESTED / UNCONFIRMED"
            summary_verdict = "Insufficient authoritative verification or conflicting news accounts."
            key_findings.append("Factual basis lacks strong independent consensus corroboration.")

        # Build transparent mathematical audit explanation
        math_str = (
            f"C_final = (0.70 × {s_evidence:.1f}) + (0.30 × {w_origin:.1f}) - (0.25 × {m_index:.1f}) "
            f"= {0.70 * s_evidence:.1f} + {0.30 * w_origin:.1f} - {m_penalty:.1f} = {final_score:.1f}/100"
        )

        return CredibilityAssessment(
            final_score=final_score,
            verdict=verdict,
            verdict_badge=verdict_badge,
            summary_verdict=summary_verdict,
            evidence_score=s_evidence,
            origin_score=w_origin,
            manipulation_index=m_index,
            manipulation_penalty=m_penalty,
            total_evidence_sources=ev_metrics["total"],
            supporting_sources_count=ev_metrics["supports"],
            refuting_sources_count=ev_metrics["refutes"],
            neutral_sources_count=ev_metrics["neutral"],
            weighted_consensus_phi=phi_bar,
            math_formula_explanation=math_str,
            key_findings=key_findings
        )
