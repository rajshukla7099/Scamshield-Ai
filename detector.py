"""
ScamShield AI - Detection Module Re-export
Maintains compatibility with legacy imports while routing to detection.scanner
"""

from detection.scanner import (
    URLScanner,
    MessageScanner,
    AIExplainer,
    detect_scam,
    calculate_entropy,
    levenshtein_distance,
    HIGH_RISK_TLDS,
    KNOWN_SHORTENERS,
    OFFICIAL_BRANDS,
    SUSPICIOUS_PATH_KEYWORDS,
    SAMPLE_TEST_CASES
)

__all__ = [
    "URLScanner",
    "MessageScanner",
    "AIExplainer",
    "detect_scam",
    "calculate_entropy",
    "levenshtein_distance",
    "HIGH_RISK_TLDS",
    "KNOWN_SHORTENERS",
    "OFFICIAL_BRANDS",
    "SUSPICIOUS_PATH_KEYWORDS",
    "SAMPLE_TEST_CASES"
]
