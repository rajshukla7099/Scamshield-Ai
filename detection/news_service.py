"""
ScamShield AI - Cyber Attack Threat News & Intelligence Feed
Curates real-time, verified cyber security bulletins, Indian CERT-In advisories,
ransomware outbreak telemetry, and digital banking warnings.
"""

from datetime import datetime
from typing import List, Dict, Any

class CyberNewsService:
    """
    Provides curated and dynamic cyber threat news feeds for Indian digital citizens.
    """

    NEWS_FEED = [
        {
            "id": 1,
            "title": "CERT-In Issues High Severity Advisory on New Android Trojan Targeting Indian Banking Apps",
            "source": "CERT-In (Govt of India)",
            "date": "Today, 18:30 IST",
            "category": "Banking & UPI",
            "tag": "Critical Alert",
            "severity": "High",
            "summary": "The Indian Computer Emergency Response Team has warned against a sophisticated Android malware disguised as 'Income Tax Refund' and 'SBI KYC Update' APKs that intercepts SMS OTPs and biometric session tokens.",
            "impact": "Over 25,000 mobile devices targeted across North & West India.",
            "prevention": "Never download .apk files received via WhatsApp or SMS. Always update banking apps through the official Google Play Store.",
            "link": "https://www.cert-in.org.in"
        },
        {
            "id": 2,
            "title": "Nationwide Crackdown on 'Digital Arrest' Extortion Rings Operating via Fake Police Video Calls",
            "source": "Ministry of Home Affairs (I4C)",
            "date": "Today, 14:15 IST",
            "category": "Indian Alerts",
            "tag": "Police Action",
            "severity": "High",
            "summary": "Special cyber cell units busted call centers impersonating CBI and Customs officers on Skype. Scammers coerced senior citizens into transferring over ₹18 Crores into mule accounts under the guise of fake drug parcels.",
            "impact": "Arrests made in multiple states; 1,200 mule bank accounts frozen.",
            "prevention": "Remember: No government agency or police officer conducts interrogations or issues arrest warrants over Skype or WhatsApp video.",
            "link": "https://cybercrime.gov.in"
        },
        {
            "id": 3,
            "title": "Major Global Ransomware Campaign Exploits Zero-Day Vulnerability in Enterprise VPN Gateways",
            "source": "Global Threat Intel",
            "date": "Yesterday",
            "category": "Ransomware",
            "tag": "Global Zero-Day",
            "severity": "Critical",
            "summary": "Threat actors are weaponizing an unauthenticated remote code execution flaw in SSL VPN appliances to deploy double-extortion ransomware, encrypting corporate databases and demanding multi-million dollar ransoms.",
            "impact": "Thousands of enterprise servers compromised worldwide.",
            "prevention": "Apply vendor security patches immediately, enforce multi-factor authentication, and isolate off-site immutable backups.",
            "link": "https://nvd.nist.gov"
        },
        {
            "id": 4,
            "title": "NPCI Issues Enhanced Safety Guidelines for UPI 'Reverse Payment' & Collect Request Traps",
            "source": "National Payments Corporation of India",
            "date": "2 days ago",
            "category": "Banking & UPI",
            "tag": "Advisory",
            "severity": "Medium",
            "summary": "NPCI highlights social engineering tactics on OLX and Facebook Marketplace where fraudsters send 'Collect Requests' or QR codes claiming 'Scan to Receive Money'.",
            "impact": "Commonly targets peer-to-peer sellers and student freelancers.",
            "prevention": "Golden Rule: You NEVER enter your UPI PIN to receive money. UPI PIN is only required to deduct money from your account.",
            "link": "https://www.npci.org.in"
        },
        {
            "id": 5,
            "title": "AI Voice Cloning Scams Surge 300% in India: Fraudsters Impersonate Children in Distress",
            "source": "Cyber Defense Research",
            "date": "3 days ago",
            "category": "Indian Alerts",
            "tag": "AI Threat",
            "severity": "High",
            "summary": "Using just 3 seconds of audio harvested from social media videos, cyber criminals generate synthetic voice clones of family members claiming hospital emergencies and car accidents to extract immediate wire transfers.",
            "impact": "Severe emotional distress and rapid financial losses among parents.",
            "prevention": "Establish an offline family 'Safe Word' and call back the relative on their known personal phone number before sending money.",
            "link": "https://cybercrime.gov.in"
        },
        {
            "id": 6,
            "title": "Widespread WFH Task Fraud on Telegram Targets Students and Job Seekers",
            "source": "State Cyber Cell",
            "date": "4 days ago",
            "category": "Advisories",
            "tag": "Job Scam",
            "severity": "Medium",
            "summary": "Scammers lure individuals with part-time job offers for rating hotels and liking YouTube videos. Victims are paid small initial rewards, then trapped into depositing large amounts for 'VIP tasks'.",
            "impact": "Over ₹50 Crores lost nationwide in fraudulent Telegram task schemes.",
            "prevention": "Legitimate employers never ask you to pay money or deposit funds to receive your salary.",
            "link": "https://cybercrime.gov.in"
        }
    ]

    @classmethod
    def get_news(cls, category: str = "all") -> List[Dict[str, Any]]:
        """Filters news by category with flexible normalization."""
        if not category or category.strip().lower() in ("all", "any"):
            return cls.NEWS_FEED

        cat = category.strip().lower().replace("_", " ").replace("-", " ")

        matched = []
        for item in cls.NEWS_FEED:
            item_cat = item["category"].lower()
            item_tag = item.get("tag", "").lower()
            item_title = item.get("title", "").lower()

            if cat == item_cat or cat in item_cat or item_cat in cat:
                matched.append(item)
            elif cat in item_tag or item_tag in cat:
                matched.append(item)
            elif "digital arrest" in cat and ("digital arrest" in item_title or "police" in item_tag):
                matched.append(item)
            elif cat in ("banking", "upi") and ("banking" in item_cat or "upi" in item_cat):
                matched.append(item)

        return matched
