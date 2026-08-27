"""
High-Performance Source Reputation Lookup Engine & MBFC Database Interface
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from ..config import MBFC_DB_PATH, TLD_CREDIBILITY_FALLBACKS
from ..utils.url_helper import extract_canonical_domain, extract_domain_parts, is_trusted_tld
from .schema import SourceReputation, FactualReportingTier, BiasTier

logger = logging.getLogger(__name__)


class SourceReputationDB:
    """
    Sub-millisecond source reputation lookup engine with multi-tier resolution:
    1. Direct Canonical Domain Match
    2. Apex Domain Match
    3. Wildcard Subdomain Match
    4. Authoritative TLD Fallback (.gov, .edu, .mil)
    5. Safe Default Unverified Fallback
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or MBFC_DB_PATH
        self._memory_cache: Dict[str, SourceReputation] = {}
        self._conn: Optional[sqlite3.Connection] = None

    def _get_connection(self) -> sqlite3.Connection:
        """Returns or opens an SQLite connection."""
        if self._conn is None:
            if not self.db_path.exists():
                raise FileNotFoundError(
                    f"MBFC Database not found at {self.db_path}. Please run build_mbfc_db.py first."
                )
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _row_to_model(self, row: sqlite3.Row, lookup_method: str = "direct_match") -> SourceReputation:
        """Converts an SQLite row to a SourceReputation model."""
        return SourceReputation(
            domain=row["domain"],
            source_name=row["source_name"] or "",
            bias=row["bias"] or "unknown",
            factual_reporting=row["factual_reporting"] or "unknown",
            credibility_score=float(row["credibility_score"]),
            credibility_rating=row["credibility_rating"] or "Unverified",
            country=row["country"] or "unknown",
            press_freedom=row["press_freedom"] or "unknown",
            media_type=row["media_type"] or "website",
            popularity=row["popularity"] or "unknown",
            is_satire=bool(row["is_satire"]),
            is_conspiracy=bool(row["is_conspiracy"]),
            is_fallback=bool(row["is_fallback"]),
            lookup_method=lookup_method,
            notes=row["notes"] or ""
        )

    def lookup(self, url_or_domain: str) -> SourceReputation:
        """
        Looks up a domain or URL's reputation.
        Returns a SourceReputation record with credibility score and bias.
        """
        if not url_or_domain:
            return self._create_fallback_reputation("unknown", "Empty domain provided")

        canonical = extract_canonical_domain(url_or_domain)
        
        # Check in-memory cache first (<0.01ms)
        if canonical in self._memory_cache:
            return self._memory_cache[canonical]

        conn = self._get_connection()
        cursor = conn.cursor()

        # 1. Direct match on canonical domain
        cursor.execute("SELECT * FROM sources WHERE domain = ? LIMIT 1", (canonical,))
        row = cursor.fetchone()
        if row:
            rep = self._row_to_model(row, lookup_method="direct_match")
            self._memory_cache[canonical] = rep
            return rep

        # 2. Check apex domain parts
        sub, dom, suffix = extract_domain_parts(url_or_domain)
        apex = f"{dom}.{suffix}" if dom and suffix else canonical
        if apex != canonical:
            cursor.execute("SELECT * FROM sources WHERE domain = ? LIMIT 1", (apex,))
            row = cursor.fetchone()
            if row:
                rep = self._row_to_model(row, lookup_method="apex_match")
                self._memory_cache[canonical] = rep
                return rep

        # 3. Wildcard domain match (e.g. if db has nytimes.com, match any.sub.nytimes.com)
        cursor.execute("SELECT * FROM sources WHERE ? LIKE '%' || domain LIMIT 1", (canonical,))
        row = cursor.fetchone()
        if row:
            rep = self._row_to_model(row, lookup_method="wildcard_match")
            self._memory_cache[canonical] = rep
            return rep

        # 4. Authoritative TLD Fallback (.gov, .edu, .mil, .int)
        is_trusted, matched_tld, tld_score = is_trusted_tld(url_or_domain)
        if is_trusted:
            rep = SourceReputation(
                domain=canonical,
                source_name=f"Official .{matched_tld.upper()} Entity",
                bias="neutral",
                factual_reporting="high",
                credibility_score=tld_score,
                credibility_rating="High Credibility (Institutional)",
                country="institutional",
                press_freedom="mostly free",
                media_type="institutional/governmental",
                popularity="high",
                is_satire=False,
                is_conspiracy=False,
                is_fallback=True,
                lookup_method="tld_fallback",
                notes=f"Reputation inferred from authoritative .{matched_tld} TLD"
            )
            self._memory_cache[canonical] = rep
            return rep

        # 5. Default Unverified Fallback
        rep = self._create_fallback_reputation(canonical, "Domain not listed in MBFC database")
        self._memory_cache[canonical] = rep
        return rep

    def _create_fallback_reputation(self, domain: str, reason: str) -> SourceReputation:
        """Constructs a safe default unverified reputation model."""
        return SourceReputation(
            domain=domain,
            source_name=domain.split(".")[0].replace("-", " ").title() if "." in domain else domain,
            bias="unknown",
            factual_reporting="unknown",
            credibility_score=0.50,
            credibility_rating="Unverified Source",
            country="unknown",
            press_freedom="unknown",
            media_type="unknown",
            popularity="unknown",
            is_satire=False,
            is_conspiracy=False,
            is_fallback=True,
            lookup_method="unlisted_fallback",
            notes=reason
        )

    def batch_lookup(self, urls_or_domains: List[str]) -> List[SourceReputation]:
        """Performs batch lookups for multiple sources in one call."""
        return [self.lookup(item) for item in urls_or_domains]

    def search_domains(self, query: str, limit: int = 10) -> List[SourceReputation]:
        """Searches domain names or source names by fuzzy substring."""
        clean_query = f"%{query.strip().lower()}%"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM sources 
            WHERE domain LIKE ? OR source_name LIKE ? 
            ORDER BY credibility_score DESC 
            LIMIT ?
            """,
            (clean_query, clean_query, limit)
        )
        rows = cursor.fetchall()
        return [self._row_to_model(r, lookup_method="search") for r in rows]

    def get_statistics(self) -> Dict[str, Any]:
        """Returns comprehensive aggregate statistics of the database."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM sources")
        total_sources = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT factual_reporting, COUNT(*) as count 
            FROM sources 
            GROUP BY factual_reporting 
            ORDER BY count DESC
        """)
        factuality_dist = {r["factual_reporting"]: r["count"] for r in cursor.fetchall()}

        cursor.execute("""
            SELECT bias, COUNT(*) as count 
            FROM sources 
            GROUP BY bias 
            ORDER BY count DESC
        """)
        bias_dist = {r["bias"]: r["count"] for r in cursor.fetchall()}

        cursor.execute("""
            SELECT country, COUNT(*) as count 
            FROM sources 
            WHERE country != 'unknown' 
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 10
        """)
        top_countries = {r["country"]: r["count"] for r in cursor.fetchall()}

        cursor.execute("SELECT AVG(credibility_score) as avg_score FROM sources")
        avg_score = round(float(cursor.fetchone()["avg_score"] or 0.0), 3)

        cursor.execute("SELECT COUNT(*) as satire_count FROM sources WHERE is_satire = 1")
        satire_count = cursor.fetchone()["satire_count"]

        cursor.execute("SELECT COUNT(*) as conspiracy_count FROM sources WHERE is_conspiracy = 1")
        conspiracy_count = cursor.fetchone()["conspiracy_count"]

        return {
            "total_sources": total_sources,
            "average_credibility_score": avg_score,
            "factuality_distribution": factuality_dist,
            "bias_distribution": bias_dist,
            "top_countries": top_countries,
            "satire_sources": satire_count,
            "conspiracy_sources": conspiracy_count,
        }

    def close(self):
        """Closes connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
