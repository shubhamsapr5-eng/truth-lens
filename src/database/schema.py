"""
Data Models and Database Schemas for PSAIAC_61 Source Reputation
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class FactualReportingTier(str, Enum):
    VERY_HIGH = "very high"
    HIGH = "high"
    MOSTLY_FACTUAL = "mostly factual"
    MIXED = "mixed"
    LOW = "low"
    VERY_LOW = "very low"
    CONSPIRACY = "conspiracy-pseudoscience"
    SATIRE = "satire"
    UNKNOWN = "unknown"


class BiasTier(str, Enum):
    LEFT = "left"
    LEFT_CENTER = "left-center"
    LEAST_BIASED = "least biased"
    NEUTRAL = "neutral"
    RIGHT_CENTER = "right-center"
    RIGHT = "right"
    EXTREME_LEFT = "extreme left"
    EXTREME_RIGHT = "extreme right"
    QUESTIONABLE = "questionable sources"
    CONSPIRACY = "conspiracy/pseudoscience"
    PRO_SCIENCE = "pro-science"
    SATIRE = "satire"
    UNKNOWN = "unknown"


class SourceReputation(BaseModel):
    """Normalized source reputation record."""
    domain: str
    source_name: str = ""
    bias: str = "unknown"
    factual_reporting: str = "unknown"
    credibility_score: float = Field(default=0.50, ge=0.0, le=1.0)  # Normalized 0.0 - 1.0
    credibility_rating: str = "Unverified"
    country: str = "unknown"
    press_freedom: str = "unknown"
    media_type: str = "website"
    popularity: str = "unknown"
    is_satire: bool = False
    is_conspiracy: bool = False
    is_fallback: bool = False
    lookup_method: str = "direct_match"  # direct_match, apex_match, subdomain_match, tld_fallback, unlisted
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @property
    def percentage_score(self) -> float:
        """Returns 0-100 score."""
        return round(self.credibility_score * 100, 1)

    @property
    def weight_factor(self) -> float:
        """Weight factor used in final corroboration aggregation formula."""
        # Satire and conspiracy get zero/near-zero weight
        if self.is_satire:
            return 0.0
        if self.is_conspiracy:
            return 0.05
        return self.credibility_score
