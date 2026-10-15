"""
Factual Claim Extraction Module for TruthLens (65% Milestone)

Extracts verifiable declarative claims from raw news articles or unstructured paragraphs.
Employs named entity recognition (NER), numerical and temporal pattern matching,
and factual assertion heuristics to separate testable claims from opinions and noise.
"""

import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ExtractedClaim(BaseModel):
    """Structured representation of an extracted factual claim."""
    claim_id: int
    text: str
    salience_score: float = Field(default=0.5, ge=0.0, le=1.0)
    entities: List[str] = Field(default_factory=list)
    has_numbers: bool = False
    has_temporal_marker: bool = False
    is_primary: bool = False
    reasoning: str = ""


# Factual action and assertion verbs that typically signify empirical claims
FACTUAL_VERBS = {
    "announce", "announced", "announces", "announcing",
    "report", "reported", "reports", "reporting",
    "confirm", "confirmed", "confirms", "confirming",
    "discover", "discovered", "discovers", "discovering",
    "sign", "signed", "signs", "signing",
    "approve", "approved", "approves", "approving",
    "launch", "launched", "launches", "launching",
    "declare", "declared", "declares", "declaring",
    "increase", "increased", "increases", "increasing",
    "decrease", "decreased", "decreases", "decreasing",
    "fail", "failed", "fails", "failing",
    "pass", "passed", "passes", "passing",
    "kill", "killed", "kills", "killing",
    "elect", "elected", "elects", "electing",
    "vote", "voted", "votes", "voting",
    "release", "released", "releases", "releasing",
    "publish", "published", "publishes", "publishing",
    "state", "stated", "states", "stating",
    "conclude", "concluded", "concludes", "concluding",
    "ban", "banned", "bans", "banning"
}

# Subjective opinion markers that disqualify or downgrade sentences
OPINION_MARKERS = [
    r"\bi think\b", r"\bin my opinion\b", r"\bi feel that\b",
    r"\bit seems to me\b", r"\bi believe\b", r"\bpersonally\b",
    r"\barguably\b", r"\bi hope\b", r"\bi suspect\b", r"\bwe might think\b"
]


class ClaimExtractor:
    """
    Extracts, ranks, and filters candidate factual claims from text.
    Uses spaCy for linguistic analysis if available, with robust regex fallbacks.
    """

    def __init__(self, use_spacy: bool = True):
        self._nlp = None
        if use_spacy:
            try:
                import spacy
                self._nlp = spacy.load("en_core_web_sm")
            except Exception as e:
                # Fallback to heuristic parser if spaCy model is unavailable
                self._nlp = None

    def extract_claims(self, text: str, max_claims: int = 4) -> List[ExtractedClaim]:
        """
        Parses text, splits into candidate sentences, scores factual assertiveness,
        and returns the top ranked testable claims.
        """
        clean_text = text.strip()
        if not clean_text:
            return []

        # 1. Segment text into candidate sentences
        sentences = self._segment_sentences(clean_text)
        if not sentences:
            return []

        scored_claims: List[ExtractedClaim] = []

        for idx, sentence in enumerate(sentences):
            s_clean = sentence.strip()
            # Basic validation: sentence length
            words = s_clean.split()
            if len(words) < 3 or len(words) > 75:
                continue

            # Exclude interrogative or rhetorical questions
            if s_clean.endswith("?"):
                continue

            # Exclude overt subjective opinion starters
            is_opinion = any(re.search(pat, s_clean, flags=re.IGNORECASE) for pat in OPINION_MARKERS)
            if is_opinion:
                continue

            # Analyze sentence
            claim_obj = self._analyze_candidate_sentence(idx + 1, s_clean)
            scored_claims.append(claim_obj)

        # Fallback: if no claim was extracted, check if any sentence has at least 3 words and is declarative
        valid_fallback = [
            s for s in sentences
            if len(s.split()) >= 3 and not s.endswith("?") and not any(re.search(pat, s, flags=re.IGNORECASE) for pat in OPINION_MARKERS)
        ]
        if not scored_claims and valid_fallback:
            fallback_claim = self._analyze_candidate_sentence(1, valid_fallback[0])
            fallback_claim.salience_score = max(0.50, fallback_claim.salience_score)
            scored_claims.append(fallback_claim)

        # Sort claims by factual salience descending
        scored_claims.sort(key=lambda c: c.salience_score, reverse=True)

        # Mark the highest-scoring candidate as the primary claim
        if scored_claims:
            scored_claims[0].is_primary = True

        return scored_claims[:max_claims]

    def _segment_sentences(self, text: str) -> List[str]:
        """Segments text into sentences using spaCy if loaded, else regex."""
        if self._nlp:
            doc = self._nlp(text)
            return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        # Robust regex sentence boundary splitter
        raw_sents = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in raw_sents if s.strip()]

    def _analyze_candidate_sentence(self, claim_id: int, sentence: str) -> ExtractedClaim:
        """Evaluates factual characteristics and computes a salience score (0.0 to 1.0)."""
        entities: List[str] = []
        tokens_lower = set(re.findall(r'\b[a-zA-Z]+\b', sentence.lower()))
        
        # Check for numbers, statistics, percentages, years
        has_numbers = bool(re.search(r'\b\d+(?:[\.,]\d+)?%?\b', sentence))
        has_temporal = bool(re.search(r'\b(19\d\d|20\d\d|january|february|march|april|may|june|july|august|september|october|november|december|yesterday|today|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', sentence, re.IGNORECASE))

        # Count factual assertion verbs
        matched_verbs = tokens_lower.intersection(FACTUAL_VERBS)

        # Entity extraction via spaCy or Capitalized N-Gram heuristic
        if self._nlp:
            doc = self._nlp(sentence)
            for ent in doc.ents:
                if ent.label_ in {"PERSON", "ORG", "GPE", "NORP", "FAC", "LOC", "EVENT", "DATE", "MONEY", "PERCENT"}:
                    entities.append(f"{ent.text} ({ent.label_})")
        else:
            # Fallback NER: sequence of Titlecase words
            title_matches = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', sentence)
            for tm in title_matches:
                if tm.lower() not in {"the", "a", "an", "this", "that", "these", "those"}:
                    entities.append(tm)

        # Deduplicate entities
        clean_entities = list(dict.fromkeys(entities))

        # Calculate Salience Score:
        # Base score = 0.40
        # +0.20 for named entities present
        # +0.15 for numerical or statistical data
        # +0.15 for presence of factual assertion verb
        # +0.10 for temporal reference (timestamped event)
        score = 0.35
        reasons = []

        if clean_entities:
            score += 0.22
            reasons.append(f"{len(clean_entities)} named entities")
        if has_numbers:
            score += 0.18
            reasons.append("numerical/statistical data")
        if matched_verbs:
            score += 0.15
            reasons.append(f"assertion verbs ({', '.join(list(matched_verbs)[:2])})")
        if has_temporal:
            score += 0.10
            reasons.append("temporal reference")

        # Normalize within [0.0, 1.0]
        final_score = round(min(score, 1.0), 2)
        reason_str = ", ".join(reasons) if reasons else "Declarative assertion"

        return ExtractedClaim(
            claim_id=claim_id,
            text=sentence,
            salience_score=final_score,
            entities=clean_entities[:5],
            has_numbers=has_numbers,
            has_temporal_marker=has_temporal,
            is_primary=False,
            reasoning=reason_str
        )
