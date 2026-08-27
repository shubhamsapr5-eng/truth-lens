"""
Manipulation & Sensationalism Indicator Detection Engine for PSAIAC_61
"""

import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field

from ..config import LEXICONS_PATH


class ManipulationReport(BaseModel):
    """Structured report on manipulation and sensationalism indicators."""
    overall_manipulation_score: float = Field(default=0.0, ge=0.0, le=100.0)  # 0 to 100
    risk_level: str = "Low"  # Low, Moderate, High, Severe
    sensationalism_score: float = 0.0
    fear_urgency_score: float = 0.0
    conspiracy_score: float = 0.0
    pseudoscience_score: float = 0.0
    stylistic_score: float = 0.0
    flagged_phrases: List[Dict[str, Any]] = Field(default_factory=list)
    stylistic_flags: List[str] = Field(default_factory=list)
    summary_warning: Optional[str] = None


def _match_term(term: str, text: str) -> int:
    """Matches a term (keyword or phrase) respecting word boundaries."""
    if not term or not text:
        return 0
    t_clean = term.strip().lower()
    escaped = re.escape(t_clean)
    # Check if first and last characters are alphanumeric
    prefix = r"\b" if t_clean[0].isalnum() else r"(?:^|\s)"
    suffix = r"\b" if t_clean[-1].isalnum() else r"(?:$|\s|[.,!?;:])"
    pattern = prefix + escaped + suffix
    return len(re.findall(pattern, text.lower()))


class ManipulationDetector:
    """
    Detects linguistic manipulation, clickbait framing, emotional urgency,
    and sensationalism patterns in news headlines and article bodies.
    """

    def __init__(self, lexicons_path: Optional[Path] = None):
        self.lexicons_path = lexicons_path or LEXICONS_PATH
        self._lexicons: Dict[str, Any] = self._load_lexicons()

    def _load_lexicons(self) -> Dict[str, Any]:
        """Loads manipulation lexicons from JSON."""
        if not self.lexicons_path.exists():
            return {}
        try:
            with open(self.lexicons_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def analyze(self, headline: str = "", body: str = "") -> ManipulationReport:
        """
        Analyzes headline and body text for manipulative patterns.
        Headline is weighted heavier (2.5x) as clickbait/manipulation concentrates in headlines.
        """
        combined_text = f"{headline} {body}".strip()
        if not combined_text:
            return ManipulationReport()

        categories = self._lexicons.get("categories", {})
        flagged_phrases = []
        category_scores: Dict[str, float] = {}

        # 1. Lexical Pattern & Keyword Matching
        for cat_name, cat_data in categories.items():
            phrases = cat_data.get("phrases", [])
            keywords = cat_data.get("keywords", [])
            cat_matches = 0

            # Match multi-word phrases (higher weight)
            for phrase in phrases:
                h_hits = _match_term(phrase, headline) if headline else 0
                b_hits = _match_term(phrase, body) if body else 0
                if h_hits > 0:
                    cat_matches += h_hits * 3.0
                    flagged_phrases.append({
                        "term": phrase,
                        "type": "phrase",
                        "category": cat_name,
                        "location": "headline",
                        "severity": "high"
                    })
                if b_hits > 0:
                    cat_matches += b_hits * 1.5
                    flagged_phrases.append({
                        "term": phrase,
                        "type": "phrase",
                        "category": cat_name,
                        "location": "body",
                        "severity": "medium"
                    })

            # Match single-word buzzwords/keywords
            for kw in keywords:
                h_hits = _match_term(kw, headline) if headline else 0
                b_hits = _match_term(kw, body) if body else 0
                if h_hits > 0:
                    cat_matches += h_hits * 2.0
                    flagged_phrases.append({
                        "term": kw,
                        "type": "keyword",
                        "category": cat_name,
                        "location": "headline",
                        "severity": "high"
                    })
                if b_hits > 0:
                    cat_matches += b_hits * 1.0
                    flagged_phrases.append({
                        "term": kw,
                        "type": "keyword",
                        "category": cat_name,
                        "location": "body",
                        "severity": "low"
                    })

            # Calculate raw category score (capped at 100)
            category_scores[cat_name] = min(cat_matches * 20.0, 100.0)

        # 2. Stylistic Markers Analysis
        stylistic_flags = []
        stylistic_score = 0.0

        # Excessive Punctuation (e.g. '!!!', '???', '!?!')
        punct_matches = re.findall(r"([!?]{2,})", combined_text)
        if punct_matches:
            stylistic_score += min(len(punct_matches) * 25.0, 60.0)
            stylistic_flags.append(f"Excessive punctuation found ({len(punct_matches)} occurrences: {', '.join(set(punct_matches))})")

        # ALL CAPS Words in headline
        if headline:
            words = headline.split()
            caps_words = [w for w in words if len(w) > 3 and w.isupper() and w.isalpha()]
            if len(caps_words) >= 2:
                stylistic_score += min(len(caps_words) * 30.0, 60.0)
                stylistic_flags.append(f"Multiple ALL-CAPS words in headline: {', '.join(caps_words)}")

        stylistic_score = min(stylistic_score, 100.0)

        # 3. Overall Weighted Score Calculation
        s_score = category_scores.get("sensationalism_clickbait", 0.0)
        f_score = category_scores.get("fear_and_urgency", 0.0)
        c_score = category_scores.get("conspiracy_and_paranoia", 0.0)
        p_score = category_scores.get("pseudoscience_miracle", 0.0)

        # Active category count to amplify multi-vector manipulation
        active_cats = sum(1 for sc in [s_score, f_score, c_score, p_score] if sc > 0)
        coordination_bonus = max(0, (active_cats - 1) * 8.0)

        raw_overall = (
            s_score * 0.35 +
            f_score * 0.25 +
            c_score * 0.25 +
            p_score * 0.15 +
            stylistic_score * 0.25 +
            coordination_bonus
        )
        overall_score = min(round(raw_overall, 1), 100.0)

        # Risk Classification
        if overall_score >= 60.0:
            risk_level = "Severe Manipulation Risk"
            summary = "High density of sensationalist, conspiratorial, or panic-inducing triggers detected."
        elif overall_score >= 35.0:
            risk_level = "Moderate Manipulation Risk"
            summary = "Notable clickbait phrasing and emotional amplification detected."
        elif overall_score >= 12.0:
            risk_level = "Mild Sensationalism"
            summary = "Slight sensationalist tone or emphasis markers detected."
        else:
            risk_level = "Low / Standard Journalistic"
            summary = "Clean language with minimal or no manipulation indicators detected."

        return ManipulationReport(
            overall_manipulation_score=overall_score,
            risk_level=risk_level,
            sensationalism_score=s_score,
            fear_urgency_score=f_score,
            conspiracy_score=c_score,
            pseudoscience_score=p_score,
            stylistic_score=stylistic_score,
            flagged_phrases=flagged_phrases,
            stylistic_flags=stylistic_flags,
            summary_warning=summary
        )
