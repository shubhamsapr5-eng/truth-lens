"""
Robust URL and Domain Extraction Helpers for PSAIAC_61
"""

import re
from urllib.parse import urlparse
from typing import Tuple, Optional

try:
    import tldextract
    _TLD_EXTRACTOR = tldextract.TLDExtract(cache_dir=False)
except ImportError:
    _TLD_EXTRACTOR = None


# Multi-part second-level domains for fallback parser
COMMON_MULTI_TLDS = {
    "co.uk", "gov.uk", "ac.uk", "org.uk", "me.uk",
    "co.in", "gov.in", "ac.in", "org.in", "net.in", "res.in", "edu.in",
    "com.au", "gov.au", "edu.au", "org.au", "net.au",
    "co.nz", "govt.nz", "ac.nz",
    "co.za", "gov.za", "ac.za",
    "co.jp", "ac.jp", "go.jp",
    "com.br", "gov.br",
    "com.sg", "gov.sg", "edu.sg",
    "com.pk", "gov.pk", "edu.pk",
    "ca", "org", "gov", "edu", "mil", "int", "net", "com", "io", "ai", "news", "info", "me"
}


def clean_url_string(input_str: str) -> str:
    """Cleans whitespace, quotes, and standardizes input."""
    if not input_str:
        return ""
    cleaned = str(input_str).strip().lower()
    # Remove leading @, quotes, angle brackets
    cleaned = re.sub(r"^[@\"'<(\[]+|[\"'>)\]]+$", "", cleaned)
    # If no protocol is present, add http:// to help urlparse
    if not re.match(r"^[a-zA-Z]+://", cleaned):
        cleaned = "http://" + cleaned
    return cleaned


def extract_domain_parts(url_or_domain: str) -> Tuple[str, str, str]:
    """
    Extracts (subdomain, domain, suffix) from a given URL or domain string.
    Example: 'https://edition.cnn.com/world' -> ('edition', 'cnn', 'com')
    """
    cleaned = clean_url_string(url_or_domain)
    if not cleaned:
        return ("", "", "")

    if _TLD_EXTRACTOR:
        try:
            res = _TLD_EXTRACTOR(cleaned)
            return (res.subdomain, res.domain, res.suffix)
        except Exception:
            pass

    # Fallback regex & parse
    parsed = urlparse(cleaned)
    hostname = parsed.hostname or parsed.path.split("/")[0].split(":")[0]
    hostname = re.sub(r"^www\.", "", hostname)
    
    parts = hostname.split(".")
    if len(parts) == 1:
        return ("", parts[0], "")
    elif len(parts) == 2:
        return ("", parts[0], parts[1])
    else:
        # Check two-part TLDs (e.g., co.uk, gov.in)
        last_two = f"{parts[-2]}.{parts[-1]}"
        if last_two in COMMON_MULTI_TLDS and len(parts) >= 3:
            domain = parts[-3]
            subdomain = ".".join(parts[:-3])
            suffix = last_two
        else:
            domain = parts[-2]
            subdomain = ".".join(parts[:-2])
            suffix = parts[-1]
        return (subdomain, domain, suffix)


def extract_canonical_domain(url_or_domain: str) -> str:
    """
    Returns registered apex domain: e.g., 'edition.cnn.com' -> 'cnn.com',
    'https://news.bbc.co.uk/story123' -> 'bbc.co.uk'.
    """
    if not url_or_domain:
        return ""

    raw_input = str(url_or_domain).strip().lower()
    # Strip protocol and paths if plain string passed
    raw_input = re.sub(r"^(https?://)?(www\.)?", "", raw_input)
    raw_input = raw_input.split("/")[0].split("?")[0].split("#")[0].split(":")[0]

    subdomain, domain, suffix = extract_domain_parts(url_or_domain)
    if domain and suffix:
        return f"{domain}.{suffix}"
    elif domain:
        return domain
    return raw_input


def extract_full_hostname(url_or_domain: str) -> str:
    """Returns full hostname without www (e.g. 'thehindu.com', 'wire.in', 'blog.hubspot.com')."""
    cleaned = clean_url_string(url_or_domain)
    parsed = urlparse(cleaned)
    hostname = parsed.hostname or ""
    return re.sub(r"^www\.", "", hostname).lower()


def is_trusted_tld(url_or_domain: str) -> Tuple[bool, Optional[str], float]:
    """
    Checks if domain has an inherently authoritative TLD (e.g. .gov, .edu, .mil).
    Returns (is_trusted, matched_tld, default_score)
    """
    _, _, suffix = extract_domain_parts(url_or_domain)
    suffix = suffix.lower()

    if any(suffix == t or suffix.endswith("." + t) for t in ["gov", "gov.in", "gov.uk", "mil"]):
        return (True, suffix, 0.95)
    if any(suffix == t or suffix.endswith("." + t) for t in ["edu", "edu.in", "ac.in", "ac.uk"]):
        return (True, suffix, 0.90)
    if suffix == "int":
        return (True, suffix, 0.92)
    if suffix == "org":
        return (False, suffix, 0.60)
    return (False, suffix, 0.50)
