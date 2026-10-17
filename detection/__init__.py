"""
ScamShield AI - Detection Engine Package
Built for HYPNEXIS ’26 at Manipal University Jaipur
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
    "SAMPLE_TEST_CASES"
]
