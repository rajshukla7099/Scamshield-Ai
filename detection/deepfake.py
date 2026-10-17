"""
ScamShield AI - Deepfake & Impersonation Detection Engine
Analyzes AI voice cloning, digital arrest video impersonation, CEO fraud,
and synthetic media manipulation patterns without requiring paid external APIs.
"""

import re
from typing import Dict, Any, List

class DeepfakeDetector:
    """
    Forensic rule engine specialized in identifying AI-driven impersonation,
    synthetic media tactics, and high-pressure digital arrest scenarios.
    """

    DIGITAL_ARREST_PATTERNS = [
        (r"\b(cbi|ed|narcotics|ncb|police|supreme court|trai|customs|crime branch)\b", "Official Law Enforcement Impersonation", 30),
        (r"\b(digital arrest|under arrest|warrant issued|arrest warrant|non[- ]bailable)\b", "Digital Arrest Threat Indicator", 35),
        (r"\b(parcel|courier|fedex|dhl).*(drugs|narcotics|mdma|passport|illegal items)\b", "Fake Customs / Narcotics Parcel Trap", 35),
        (r"\b(skype|telegram|whatsapp video).*(statement|interrogation|investigation)\b", "Video Call Interrogation (Police Never Uses Skype)", 30),
        (r"\b(rbi|secret|safe|verification|clearance).*(account|transfer|fund|deposit)\b", "Transfer to 'RBI Verification Account' Trap", 40),
        (r"\b(camera on|do not leave|video call continuously|room locked|isolate)\b", "Surveillance & Psychological Isolation Tactic", 25),
    ]

    VOICE_CLONING_PATTERNS = [
        (r"\b(accident|hospital|emergency|police station|bail|kidnap|kidnapped)\b", "Emergency Crisis Extortion Pattern", 35),
        (r"\b(send money immediately|urgent upi|google pay fast|friend's account)\b", "Urgent Third-Party Payment Demand", 30),
        (r"\b(don't call mom|don't tell dad|don't tell anyone|phone battery low)\b", "Communication Interruption / Isolation Tactic", 25),
        (r"\b(voice sounds different|network problem|throat infection|coughing)\b", "Voice Distortion Excuse Pattern", 25),
    ]

    CEO_FRAUD_PATTERNS = [
        (r"\b(i am in a meeting|confidential task|cannot take calls|urgent request)\b", "Executive Inaccessibility Pretext", 25),
        (r"\b(apple gift card|amazon voucher|crypto|wire transfer|vendor payment)\b", "Unorthodox Corporate Payment Request", 35),
        (r"\b(do this right away|keep this between us|priority client)\b", "Authority Pressure & Secrecy", 25),
    ]

    CELEBRITY_DEEPFAKE_PATTERNS = [
        (r"\b(ambani|tata|narayana murthy|musk|modi|sachin|kohli)\b.*(trading|crypto|invest|guaranteed return)", "Celebrity Deepfake Endorsement Scam", 40),
        (r"\b(guaranteed return|10x return|rbi approved algorithm|automated wealth)\b", "High-Yield Algorithmic Promise", 30),
    ]

    @classmethod
    def analyze(cls, text: str, media_type: str = "general") -> Dict[str, Any]:
        """
        Analyzes conversational transcripts, suspect messages, or behavioral notes
        for deepfake and impersonation indicators.
        """
        cleaned = text.strip().lower()
        if not cleaned:
            return {
                "risk_score": 0,
                "risk_level": "Low",
                "impersonation_type": "None",
                "indicators": [],
                "forensic_flags": [],
                "recommendations": ["No input provided for analysis."],
                "is_deepfake_likely": False
            }

        score = 0
        indicators = []
        forensic_flags = []
        impersonation_type = "Unspecified Impersonation"

        # 1. Digital Arrest Checks
        da_matches = 0
        for pattern, title, weight in cls.DIGITAL_ARREST_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                da_matches += 1
                score += weight
                indicators.append({
                    "title": title,
                    "desc": f"Matched suspicious digital arrest signature: '{title}'",
                    "severity": "High" if weight >= 30 else "Medium",
                    "weight": weight
                })
        if da_matches >= 2:
            impersonation_type = "Digital Arrest / Law Enforcement Impersonation"

        # 2. Voice Cloning / Family Emergency Checks
        vc_matches = 0
        for pattern, title, weight in cls.VOICE_CLONING_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                vc_matches += 1
                score += weight
                indicators.append({
                    "title": title,
                    "desc": f"Matched AI voice cloning emergency extortion indicator: '{title}'",
                    "severity": "High" if weight >= 30 else "Medium",
                    "weight": weight
                })
        if vc_matches >= 2 and score > 45:
            impersonation_type = "AI Voice Cloning / Family Emergency Scam"

        # 3. CEO / Whaling Fraud Checks
        for pattern, title, weight in cls.CEO_FRAUD_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                score += weight
                indicators.append({
                    "title": title,
                    "desc": f"Matched executive impersonation pretext: '{title}'",
                    "severity": "Medium",
                    "weight": weight
                })
                if score > 40:
                    impersonation_type = "CEO Fraud / Executive Impersonation"

        # 4. Celebrity Deepfake Investment
        for pattern, title, weight in cls.CELEBRITY_DEEPFAKE_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                score += weight
                indicators.append({
                    "title": title,
                    "desc": f"Matched synthetic endorsement trading trap: '{title}'",
                    "severity": "High",
                    "weight": weight
                })
                impersonation_type = "Celebrity Deepfake Investment Fraud"

        # Deepfake Forensic Artifact Checklist
        if "video" in cleaned or "call" in cleaned or "skype" in cleaned or media_type == "video":
            forensic_flags.append("Inspect facial boundaries: AI face-swaps exhibit blurring around ears and jawline.")
            forensic_flags.append("Check eye blinking: Deepfake avatars often have irregular or zero natural micro-blinking.")
            forensic_flags.append("Audio-video sync: Look for 150ms-300ms delays between lip movements and spoken syllables.")
            forensic_flags.append("Background lighting: Synthetic video models fail to cast dynamic facial shadows from ambient room lights.")

        if "voice" in cleaned or "audio" in cleaned or media_type == "voice":
            forensic_flags.append("Voice cadence: AI voice models often lack natural breathing pauses between sentences.")
            forensic_flags.append("Background noise absence: Cloned voices are usually rendered in clinical silence without realistic environmental acoustics.")

        # Cap score
        final_score = min(score, 100)
        risk_level = "High" if final_score >= 65 else ("Medium" if final_score >= 35 else "Low")

        # Recommendations
        recommendations = []
        if risk_level == "High":
            recommendations.append("🚨 HANG UP IMMEDIATELY. Law enforcement agencies (Police, CBI, ED, Customs) NEVER conduct interrogations or arrest citizens over WhatsApp/Skype video calls.")
            recommendations.append("🛑 NEVER transfer money to any 'RBI Verification', 'Court Clearance', or 'Escrow' bank account. The RBI does not maintain citizen verification accounts.")
            recommendations.append("📞 If caller claimed to be a family member in distress, call them directly on their known regular phone number or contact another family member to verify.")
            recommendations.append("🛡️ Dial the National Cyber Helpline 1930 and file a complaint on https://cybercrime.gov.in.")
        elif risk_level == "Medium":
            recommendations.append("Request a live verification test: Ask the caller to wave their hand across their face or turn their head 90 degrees (breaks deepfake rendering).")
            recommendations.append("Establish a family 'Safe Word': Always ask for a private keyword that only real family members know.")
            recommendations.append("Independently verify phone numbers through official directories rather than numbers provided by the caller.")
        else:
            recommendations.append("No immediate deepfake or impersonation flags detected, but remain cautious with unfamiliar numbers requesting urgent funds.")

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "impersonation_type": impersonation_type if indicators else "Clean / Low Risk",
            "indicators": indicators,
            "forensic_flags": forensic_flags,
            "recommendations": recommendations,
            "is_deepfake_likely": final_score >= 60
        }
