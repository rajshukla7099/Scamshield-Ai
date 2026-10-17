"""
ScamShield AI - Detection Engine Package
Next-Generation Cyber Threat Defense & Intelligence Platform
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
from detection.deepfake import DeepfakeDetector
from detection.threat_radar import ThreatRadar
from detection.incident_dossier import IncidentDossierGenerator
from detection.news_service import CyberNewsService
from detection.chatbot_engine import ShieldBotEngine

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
    "SAMPLE_TEST_CASES",
    "DeepfakeDetector",
    "ThreatRadar",
    "IncidentDossierGenerator",
    "CyberNewsService",
    "ShieldBotEngine"
]
