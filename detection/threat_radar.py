"""
ScamShield AI - Advanced Cyber Threat & Payload Radar
Specialized detector for:
1. SQL Injection (SQLi)
2. Cross-Site Scripting (XSS)
3. Malware & Ransomware Payload Signatures (APK, double-extension, ransom notes)
4. DoS/DDoS & Brute-Force Anomaly Heuristics
5. MITM & DNS Spoofing Risk Analysis
"""

import re
from typing import Dict, Any, List

class ThreatRadar:
    """
    Advanced security engine analyzing web attack payloads, malicious code strings,
    suspicious file downloads, and network anomaly patterns.
    """

    # 1. SQL Injection Patterns
    SQLI_PATTERNS = [
        (r"(\%27)|(\')|(\-\-)|(\%23)|(#)", "SQL Meta-Characters & Comment Syntax", 25),
        (r"\b(or|and)\b\s+[\'\"]?\w+[\'\"]?\s*=\s*[\'\"]?\w+[\'\"]?", "Boolean-Based SQL Tautology (e.g. ' OR 1=1)", 35),
        (r"\b(union(\s+all)?\s+select)\b", "UNION SELECT Extraction Vector", 45),
        (r"\b(select|insert|update|delete|drop|alter|truncate|exec|execute)\b.*\b(from|into|table|database)\b", "Direct SQL Data Manipulation Command", 40),
        (r"\b(sleep|waitfor\s+delay|benchmark|pg_sleep)\b", "Time-Based Blind SQL Injection Payload", 40),
        (r"\b(information_schema|sys\.tables|sysobjects|all_tables)\b", "Database Metadata Enumeration Target", 35),
    ]

    # 2. XSS (Cross-Site Scripting) Patterns
    XSS_PATTERNS = [
        (r"<\s*script[^>]*>.*<\s*/\s*script\s*>", "Explicit Script Tag Injection", 45),
        (r"javascript\s*:\s*[^\s]+", "JavaScript URI Pseudo-Protocol Vector", 35),
        (r"\bon\w+\s*=\s*[\'\"]?[^\'\">]+[\'\"]?", "DOM Event Handler Hijacking (e.g. onload, onerror, onclick)", 40),
        (r"<\s*(iframe|object|embed|svg|img)[^>]+(src|data|href)\s*=", "Unsafe Media Object Embedding Vector", 30),
        (r"\b(document\.cookie|window\.location|eval\(|alert\(|prompt\()", "XSS Execution Primitive (Cookie Stealing / Popup)", 35),
    ]

    # 3. Malware & Ransomware Signatures
    MALWARE_PATTERNS = [
        (r"\.(apk|exe|bat|cmd|vbs|ps1|scr|pif|hta|jar|iso)$", "High-Risk Executable / APK File Extension", 40),
        (r"\b(update|install|verify|security|bank).*\.(apk|exe)\b", "Deceptive App Disguised as Security Update", 45),
        (r"\.(pdf|docx|xlsx|jpg)\.(exe|apk|scr|vbs)$", "Double Extension Camouflage Vector", 50),
        (r"\b(your files have been encrypted|pay ransom|decrypt your files|send bitcoin|readme_decrypt)\b", "Ransomware Ransom Note Signature", 50),
        (r"\b(remote support|anydesk|teamviewer|rustdesk|quicksupport).*(download|install|access)\b", "Remote Access Trojan (RAT) Social Engineering", 35),
        (r"powershell\s+(-enc|-encodedcommand|-w\s+hidden|-exec\s+bypass)", "Obfuscated PowerShell Execution Vector", 45),
    ]

    # 4. Network / DDoS / Brute-Force Anomaly Keywords
    ANOMALY_PATTERNS = [
        (r"\b(rate_limit_exceeded|too_many_requests|syn_flood|http_flood)\b", "DDoS Flood / Excessive Request Surge", 30),
        (r"\b(failed login|invalid credentials|max login attempts|account locked)\b", "Brute-Force Credential Stuffing Anomaly", 30),
        (r"\b(ssl_error|cert_invalid|untrusted_ca|man-in-the-middle|mitm)\b", "MITM / Untrusted Certificate Warning", 35),
        (r"\b(dns_mismatch|unauthorized_nameserver|cache_poisoning)\b", "DNS Spoofing / Resolution Hijack Warning", 35),
    ]

    @classmethod
    def analyze_payload(cls, input_data: str) -> Dict[str, Any]:
        """
        Inspects strings, query parameters, web logs, or file payloads for cyber attacks.
        """
        cleaned = (input_data or "").strip()
        if not cleaned:
            return {
                "risk_score": 0,
                "risk_level": "Low",
                "attack_vector": "None",
                "matched_categories": [],
                "indicators": [],
                "remediation": ["No payload provided for inspection."]
            }

        score = 0
        indicators = []
        matched_categories = set()

        # Check SQL Injection
        sqli_hits = 0
        for pattern, title, weight in cls.SQLI_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                sqli_hits += 1
                score += weight
                indicators.append({
                    "category": "SQL Injection (SQLi)",
                    "title": title,
                    "desc": f"Matched signature: '{title}'",
                    "severity": "High" if weight >= 35 else "Medium"
                })
                matched_categories.add("SQL Injection")

        # Check XSS
        xss_hits = 0
        for pattern, title, weight in cls.XSS_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                xss_hits += 1
                score += weight
                indicators.append({
                    "category": "Cross-Site Scripting (XSS)",
                    "title": title,
                    "desc": f"Matched signature: '{title}'",
                    "severity": "High" if weight >= 35 else "Medium"
                })
                matched_categories.add("Cross-Site Scripting (XSS)")

        # Check Malware & Ransomware
        malware_hits = 0
        for pattern, title, weight in cls.MALWARE_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                malware_hits += 1
                score += weight
                indicators.append({
                    "category": "Malware & Ransomware",
                    "title": title,
                    "desc": f"Matched signature: '{title}'",
                    "severity": "High" if weight >= 40 else "Medium"
                })
                matched_categories.add("Malware & Ransomware")

        # Check Anomaly
        for pattern, title, weight in cls.ANOMALY_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                score += weight
                indicators.append({
                    "category": "Network / Traffic Anomaly",
                    "title": title,
                    "desc": f"Matched network warning indicator: '{title}'",
                    "severity": "Medium"
                })
                matched_categories.add("Network Anomaly / Brute-Force")

        final_score = min(score, 100)
        risk_level = "High" if final_score >= 60 else ("Medium" if final_score >= 30 else "Low")

        remediation = []
        if "SQL Injection" in matched_categories:
            remediation.append("Implement Prepared Statements / Parameterized Queries (PDO, SQLAlchemy, ORM) to neutralize SQL metacharacters.")
        if "Cross-Site Scripting (XSS)" in matched_categories:
            remediation.append("Sanitize and HTML-encode all dynamic user inputs before rendering. Enforce a robust Content Security Policy (CSP).")
        if "Malware & Ransomware" in matched_categories:
            remediation.append("Do NOT execute or install this payload. Block APK side-loading and submit the file hash to an isolated sandbox.")
        if "Network Anomaly / Brute-Force" in matched_categories:
            remediation.append("Enforce IP rate limiting (e.g. 60 req/min), progressive account lockout, and Mandatory 2-Factor Authentication.")

        if not remediation:
            remediation.append("Payload appears within baseline safety thresholds. Continue adhering to least-privilege security policies.")

        primary_vector = list(matched_categories)[0] if matched_categories else "Benign Payload / Clean"

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "attack_vector": primary_vector,
            "matched_categories": list(matched_categories),
            "indicators": indicators,
            "remediation": remediation,
            "is_malicious": final_score >= 50
        }
