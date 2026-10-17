"""
ScamShield AI - Heuristic Detection Engine
Next-Generation Cyber Threat Defense & Intelligence Platform

Features:
- Lexical, structural, and reputation inspection for URLs
- Shannon entropy and Levenshtein distance brand impersonation
- Multi-lingual and Hinglish NLP rule matrix for SMS, WhatsApp, and email scams
- Negation-aware context evaluation (e.g. "Never share your OTP" is recognized as safety advice)
- Safe offline-first architecture with ZERO external API dependencies and ZERO SSRF risk
"""

import re
import math
from urllib.parse import urlparse
from typing import Dict, Any, List

# =====================================================================
# THREAT INTELLIGENCE & REPUTATION DATABASE (Built-in Heuristic Knowledge)
# =====================================================================

HIGH_RISK_TLDS = {
    "xyz", "top", "tk", "ml", "ga", "cf", "gq", "buzz", "fit", "work", "icu",
    "cam", "rest", "country", "click", "monster", "link", "live", "loan", "date",
    "racing", "party", "gdn", "stream", "trade", "bid", "pw", "cc", "ws", "sbs"
}

KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy", "shorturl.at",
    "goo.gl", "ow.ly", "rebrand.ly", "clck.ru", "v.gd", "trib.al", "tiny.cc",
    "shorte.st", "adf.ly", "bc.vc"
}

# Major protected brands frequently targeted by phishing campaigns in India
OFFICIAL_BRANDS = {
    "sbi": {"official_domains": ["onlinesbi.sbi", "sbi.co.in", "bank.sbi"], "name": "State Bank of India"},
    "onlinesbi": {"official_domains": ["onlinesbi.sbi", "sbi.co.in"], "name": "State Bank of India"},
    "hdfc": {"official_domains": ["hdfcbank.com", "hdfc.com"], "name": "HDFC Bank"},
    "hdfcbank": {"official_domains": ["hdfcbank.com"], "name": "HDFC Bank"},
    "icici": {"official_domains": ["icicibank.com"], "name": "ICICI Bank"},
    "icicibank": {"official_domains": ["icicibank.com"], "name": "ICICI Bank"},
    "axis": {"official_domains": ["axisbank.com"], "name": "Axis Bank"},
    "axisbank": {"official_domains": ["axisbank.com"], "name": "Axis Bank"},
    "kotak": {"official_domains": ["kotak.com"], "name": "Kotak Mahindra Bank"},
    "pnb": {"official_domains": ["pnbindia.in"], "name": "Punjab National Bank"},
    "paytm": {"official_domains": ["paytm.com", "paytmbank.com"], "name": "Paytm"},
    "phonepe": {"official_domains": ["phonepe.com"], "name": "PhonePe"},
    "gpay": {"official_domains": ["pay.google.com", "google.com"], "name": "Google Pay"},
    "google": {"official_domains": ["google.com", "google.co.in"], "name": "Google"},
    "paypal": {"official_domains": ["paypal.com"], "name": "PayPal"},
    "amazon": {"official_domains": ["amazon.in", "amazon.com"], "name": "Amazon India"},
    "flipkart": {"official_domains": ["flipkart.com"], "name": "Flipkart"},
    "netflix": {"official_domains": ["netflix.com"], "name": "Netflix"},
    "microsoft": {"official_domains": ["microsoft.com", "live.com", "office.com"], "name": "Microsoft"},
    "apple": {"official_domains": ["apple.com", "icloud.com"], "name": "Apple"},
    "indiapost": {"official_domains": ["indiapost.gov.in", "postoffice.gov.in"], "name": "India Post"},
    "incometax": {"official_domains": ["incometax.gov.in"], "name": "Income Tax Department"},
    "uidai": {"official_domains": ["uidai.gov.in"], "name": "UIDAI / Aadhaar"},
    "aadhaar": {"official_domains": ["uidai.gov.in"], "name": "UIDAI / Aadhaar"},
    "whatsapp": {"official_domains": ["whatsapp.com"], "name": "WhatsApp"},
    "telegram": {"official_domains": ["telegram.org", "t.me"], "name": "Telegram"}
}

SUSPICIOUS_PATH_KEYWORDS = {
    "login": 15, "signin": 15, "verify": 20, "verification": 20, "kyc": 25,
    "update-kyc": 30, "pan-card": 20, "aadhaar": 20, "otp": 30, "secure": 10,
    "account": 10, "banking": 15, "wallet": 20, "claim": 25, "prize": 25,
    "refund": 25, "support": 10, "confirm": 15, "bill-payment": 20, "reward": 25,
    "re-delivery": 25, "customs": 25, "apk": 30, "download-app": 25
}

# Pre-configured demonstration test samples
SAMPLE_TEST_CASES = {
    "url": [
        {
            "id": "sbi_phish",
            "label": "🏦 Fake SBI KYC Portal (.xyz)",
            "content": "http://sbi-kyc-verification-portal.xyz/login.php?user=verify",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "ip_host",
            "label": "🌐 Raw IP Phishing Host",
            "content": "http://192.168.1.105/bank/secure/login",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "india_post",
            "label": "📦 India Post Redelivery Scam (.top)",
            "content": "http://indiapost-parcel-tracking.top/re-delivery/confirm",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "shortener",
            "label": "🔗 URL Shortener Concealment",
            "content": "https://bit.ly/claim-free-iphone-reward",
            "expected_risk": "Medium",
            "is_demonstration": True
        },
        {
            "id": "legit_sbi",
            "label": "✅ Official SBI Website",
            "content": "https://www.onlinesbi.sbi/portal/index.html",
            "expected_risk": "Low",
            "is_demonstration": True
        },
        {
            "id": "legit_tech",
            "label": "✅ Safe Tech Blog",
            "content": "https://developer.mozilla.org/en-US/docs/Web/HTTP",
            "expected_risk": "Low",
            "is_demonstration": True
        }
    ],
    "message": [
        {
            "id": "electricity_scam",
            "label": "⚡ Electricity Disconnection (Hinglish)",
            "content": "Dear Consumer, Aapka bijli connection aaj raat 9:30 baje kat diya jayega kyuki pichle mahine ka bill update nahi hua. Turant officer Rahul Sharma ko call kare 9876543210 par.",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "digital_arrest",
            "label": "🚨 Digital Arrest Extortion",
            "content": "URGENT NOTICE: CBI Cyber Crime Cell has issued a non-bailable warrant for your illegal FedEx parcel containing narcotics. You are under Digital Arrest. Immediately join Skype video interrogation.",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "wfh_job",
            "label": "💼 Telegram Part-Time Job Scam",
            "content": "Part-time work from home! Earn Rs. 3000 to 5000 daily by simply liking YouTube videos. No experience needed. Join Telegram HR group @FastEarnIndia now. Pre-paid VIP tasks available.",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "upi_trap",
            "label": "📲 UPI 'Scan to Receive' Trap",
            "content": "Congratulations! You have received cashback of Rs. 2,999 on PhonePe. Scan this QR code and enter your UPI PIN to claim your refund in your bank account immediately.",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "remote_app_apk",
            "label": "📲 AnyDesk / APK Remote Access",
            "content": "Your bank account has been locked. Install QuickSupport AnyDesk app or download support.apk from http://bank-helper.xyz to unblock your account with our executive.",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "fake_customer_care",
            "label": "📞 Fake Customer Care Number",
            "content": "Swiggy refund issue? Call official customer care helpline 9823123456 immediately. Send OTP for instant wallet refund.",
            "expected_risk": "High",
            "is_demonstration": True
        },
        {
            "id": "legit_bank_sms",
            "label": "✅ Legitimate Bank Transaction SMS",
            "content": "Dear Customer, INR 1,500.00 debited from your A/C ending in 4321 at HDFC ATM on 16-OCT-26. Avail Bal: INR 24,350.00. If not done by you, SMS BLOCK to 56767. Never share your OTP.",
            "expected_risk": "Low",
            "is_demonstration": True
        }
    ]
}


def calculate_entropy(string: str) -> float:
    """Calculates the Shannon entropy of a string (measures randomness)."""
    if not string:
        return 0.0
    probabilities = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in probabilities])
    return entropy


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes Levenshtein distance to catch typosquatted brand names."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# =====================================================================
# URL SCANNER
# =====================================================================

class URLScanner:
    @staticmethod
    def analyze(url_string: str) -> Dict[str, Any]:
        """
        Safely inspects a URL string using lexical, structural, and heuristic rules.
        Never executes dangerous external HTTP fetches (protects against SSRF/Malware).
        """
        raw_url = (url_string or "").strip()
        indicators = []
        risk_score = 0
        primary_category = "Clean / Low Risk"

        if not raw_url:
            return {
                "risk_score": 0,
                "risk_level": "Low",
                "primary_category": "Empty Input",
                "indicators": [],
                "detected_indicators": [],
                "explanations": ["No input provided for analysis."],
                "recommendations": ["Please enter or paste a URL to analyze."],
                "domain": "",
                "protocol": "",
                "scan_type": "url",
                "disclaimer": "Automated preliminary heuristic assessment. Exercise vigilance."
            }

        # Auto-prefix protocol if missing for URL parsing
        parse_target = raw_url
        if not re.match(r'^[a-zA-Z]+://', raw_url):
            parse_target = "http://" + raw_url

        try:
            parsed = urlparse(parse_target)
        except Exception:
            return {
                "risk_score": 90,
                "risk_level": "High",
                "primary_category": "Malformed URL",
                "indicators": [{
                    "title": "Invalid URL Structure",
                    "severity": "High",
                    "desc": "Malformed link structure commonly used in obfuscation."
                }],
                "detected_indicators": ["Invalid URL Structure"],
                "explanations": ["The URL format is malformed or improperly encoded, often indicating an obfuscation attempt."],
                "recommendations": ["Do not attempt to open this link in any browser."],
                "domain": "Unknown",
                "protocol": "Invalid",
                "scan_type": "url",
                "disclaimer": "Automated preliminary heuristic assessment. Exercise vigilance."
            }

        hostname = (parsed.hostname or "").lower()
        path = (parsed.path or "").lower()
        query = (parsed.query or "").lower()

        # 1. Scheme Check
        protocol = parsed.scheme.lower()
        if protocol == "http":
            risk_score += 20  # Non-HTTPS is a weak indicator, not automatic proof of scam
            indicators.append({
                "title": "Unencrypted HTTP Protocol",
                "severity": "Low",
                "desc": "The link does not use TLS/HTTPS encryption. Data transmitted over HTTP can be intercepted, though older or internal sites may also lack HTTPS."
            })
        elif protocol in ["data", "javascript", "vbscript", "file"]:
            risk_score += 50
            primary_category = "Executable Script Scheme"
            indicators.append({
                "title": f"Dangerous Protocol Scheme ({protocol}:)",
                "severity": "High",
                "desc": f"Link uses an executable script or data URI protocol '{protocol}:', frequently used in Cross-Site Scripting (XSS) and local exploit execution."
            })

        # 2. IP Address as Host
        ip_v4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_v4_pattern, hostname):
            risk_score += 45
            primary_category = "Raw IP Host Phishing"
            indicators.append({
                "title": "Numerical IP Address Used as Host",
                "severity": "High",
                "desc": f"Host '{hostname}' is a raw IP address instead of a registered domain name. Legitimate institutions (banks, payment gateways) never ask users to log in directly through IP addresses."
            })

        # 3. URL Shortener Detection
        if hostname in KNOWN_SHORTENERS:
            risk_score += 25
            primary_category = "Hidden / Shortened Link"
            indicators.append({
                "title": "Concealed Destination via URL Shortener",
                "severity": "Medium",
                "desc": f"Host '{hostname}' is a URL shortening service that conceals the true landing website, commonly used to bypass SMS and email scam filters."
            })

        # 4. High Risk TLD Detection
        tld = hostname.split('.')[-1] if '.' in hostname else ""
        if tld in HIGH_RISK_TLDS:
            risk_score += 30
            primary_category = "High-Risk Domain Extension"
            indicators.append({
                "title": f"High-Risk Phishing TLD (.{tld})",
                "severity": "High",
                "desc": f"Top-level domain '.{tld}' is a cheap or disposable domain extension heavily correlated with transient malicious hosting."
            })

        # 5. Lookalike Brand Impersonation & Typosquatting
        domain_parts = hostname.split('.')
        for brand_key, brand_info in OFFICIAL_BRANDS.items():
            if brand_key in hostname:
                is_official = any(hostname == off or hostname.endswith('.' + off) for off in brand_info["official_domains"])
                if not is_official:
                    risk_score += 45
                    primary_category = f"{brand_info['name']} Impersonation"
                    indicators.append({
                        "title": f"Spoofed {brand_info['name']} Brand Identifier",
                        "severity": "High",
                        "desc": f"Domain contains the name of '{brand_info['name']}', but is NOT hosted on any authorized domain ({', '.join(brand_info['official_domains'])}). This is a strong indicator of a phishing clone."
                    })
                    break
            else:
                domain_core = domain_parts[-2] if len(domain_parts) >= 2 else hostname
                if 2 <= len(domain_core) <= 15:
                    dist = levenshtein_distance(domain_core, brand_key)
                    if 1 <= dist <= 2 and abs(len(domain_core) - len(brand_key)) <= 1:
                        risk_score += 40
                        primary_category = "Typosquatting Lookalike Domain"
                        indicators.append({
                            "title": f"Typosquatting Detected: Similar to {brand_info['name']}",
                            "severity": "High",
                            "desc": f"Domain '{domain_core}' closely resembles official brand '{brand_key}' (edit distance: {dist}), a common technique to trick users into trusting a spoofed site."
                        })
                        break

        # 6. Misleading Subdomain Chains
        if len(domain_parts) >= 4:
            risk_score += 20
            indicators.append({
                "title": "Excessive Subdomain Stacking",
                "severity": "Medium",
                "desc": f"Host '{hostname}' has {len(domain_parts)} domain segments. Attackers stack prefixes like 'paypal.com.verify.attacker.com' to deceive mobile browsers with limited address bar widths."
            })

        # 7. Punycode / Homoglyph Attack (IDN spoofing)
        if "xn--" in hostname:
            risk_score += 35
            primary_category = "Internationalized Homoglyph Spoof"
            indicators.append({
                "title": "Punycode (Homoglyph) Character Spoofing",
                "severity": "High",
                "desc": "Domain utilizes Punycode ('xn--') encoding, which can visually mimic Latin letters using Cyrillic or Greek symbols to fool visual inspection."
            })

        # 8. High Entropy (Algorithmic / DGA generation)
        entropy = calculate_entropy(hostname.replace('.', ''))
        if entropy > 3.8 and len(hostname) > 12:
            risk_score += 15
            indicators.append({
                "title": "High Domain Entropy (Random Characters)",
                "severity": "Medium",
                "desc": f"Domain name exhibits high lexical randomness (Entropy: {entropy:.2f}), typical of automated Domain Generation Algorithms (DGAs) used in malware and phishing."
            })

        # 9. Sensitive Credential Harvesting Keywords in Path/Query
        detected_keywords = []
        for kw, weight in SUSPICIOUS_PATH_KEYWORDS.items():
            if kw in path or kw in query:
                detected_keywords.append(kw)
                risk_score += min(weight, 15)

        if detected_keywords:
            risk_score += 15
            if primary_category == "Clean / Low Risk":
                primary_category = "Credential Harvesting Path"
            indicators.append({
                "title": f"Suspicious Path Keywords ({', '.join(detected_keywords[:4])})",
                "severity": "Medium",
                "desc": f"URL path or query parameters target sensitive actions ({', '.join(detected_keywords)}), frequently observed in phishing login forms."
            })

        # 10. Hyphen Overuse
        if hostname.count('-') >= 2:
            risk_score += 15
            indicators.append({
                "title": "Excessive Hyphenation in Hostname",
                "severity": "Low",
                "desc": f"Hostname contains {hostname.count('-')} hyphens, a technique frequently used to concatenate genuine company names with fraud buzzwords."
            })

        # 11. Obfuscated '@' symbol in URL
        if "@" in raw_url:
            risk_score += 35
            primary_category = "Userinfo Deceptive Authority Attack"
            indicators.append({
                "title": "Deceptive '@' Authority Character",
                "severity": "High",
                "desc": "URL contains an '@' character. In URI specifications, everything before '@' is treated as user authentication info, while the browser navigates to the host after the '@'."
            })

        # Normalize score
        risk_score = min(100, max(0, risk_score))

        # Risk Classification
        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            if not indicators:
                indicators.append({
                    "title": "No Obvious Structural Red Flags Detected",
                    "severity": "Low",
                    "desc": "URL does not match known high-risk TLDs, IP host patterns, or deceptive brand lookalike rules. Always verify the TLS certificate and destination before entering passwords."
                })

        # Explanations list
        explanations = [f"{ind['title']}: {ind['desc']}" for ind in indicators]

        # Recommendations
        recommendations = URLScanner.generate_recommendations(risk_level, primary_category)

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "primary_category": primary_category,
            "domain": hostname,
            "protocol": protocol.upper(),
            "indicators": indicators,
            "detected_indicators": [ind["title"] for ind in indicators],
            "explanations": explanations,
            "recommendations": recommendations,
            "entropy": round(entropy, 2),
            "scan_type": "url",
            "disclaimer": "This risk assessment is an automated heuristic estimation. Zero flags do not provide an absolute guarantee of safety. Exercise vigilance when entering credentials."
        }

    @staticmethod
    def generate_recommendations(risk_level: str, category: str) -> List[str]:
        recs = []
        if risk_level == "High":
            recs.append("DO NOT click or open this link in your browser.")
            recs.append("Never enter login credentials, OTPs, Aadhaar numbers, or bank card details on this page.")
            recs.append("If you already submitted sensitive financial information, immediately block your cards and freeze NetBanking via your official banking app.")
            recs.append("Report cyber fraud immediately on the National Cyber Crime Reporting Portal (cybercrime.gov.in) or call National Helpline 1930.")
        elif risk_level == "Medium":
            recs.append("Treat this link with caution. Independently search for the official organization website through a verified search engine.")
            recs.append("If this is a shortened link (bit.ly, t.co), unshorten and inspect the actual destination before navigating.")
            recs.append("Check the browser address bar for a valid TLS/SSL padlock icon registered to the genuine company.")
        else:
            recs.append("Always verify that the address bar matches the official domain before entering personal information.")
            recs.append("Keep your web browser and operating system security patches up to date.")
            recs.append("Remember that legitimate organizations never ask for your password or PIN via email or SMS.")
        return recs


# =====================================================================
# MESSAGE ANALYZER (NLP & HINGLISH/HINDI HEURISTICS)
# =====================================================================

class MessageScanner:
    RULES = [
        {
            "category": "Credential & OTP Harvesting",
            "regex": r'\b(share\s+(your\s+)?otp|enter\s+(your\s+)?(upi\s+)?pin|send\s+password|cvv\s+number|atm\s+pin|netbanking\s+password|otp\s+bhejo|otp\s+share\s+kare|pin\s+batao|pin\s+enter\s+kare|password\s+maange|ओटीपी|पिन)\b',
            "weight": 70,
            "severity": "High",
            "title": "Credential / OTP / PIN Demand",
            "desc": "The message demands personal credentials, OTP, or UPI PIN. Legitimate banks and government officials will NEVER ask you to disclose an OTP or PIN over chat or call."
        },
        {
            "category": "Urgent Utility / Electricity Power Cut",
            "regex": r'\b(electricity\s+(bill|power|connection)|bijli\s+(bill|connection)|power\s+cut|disconnected\s+tonight|kat\s+diya\s+jayega|aaj\s+raat|light\s+kat|officer\s+rahul|power\s+sub-station|contact\s+electricity\s+officer)\b',
            "weight": 55,
            "severity": "High",
            "title": "Electricity / Utility Disconnection Threat",
            "desc": "Threatens immediate power disconnection within hours and directs contact to an individual mobile number. State power utilities never threaten power cuts via informal personal SMS."
        },
        {
            "category": "Digital Arrest / Law Enforcement Impersonation",
            "regex": r'\b(digital\s+arrest|cbi(\s+officer|\s+cyber)?|cyber\s+crime\s+cell|narcotics\s+control|customs\s+department|illegal\s+(parcel|package|drugs)|fedex\s+parcel|police\s+warrant|court\s+arrest|rbi\s+escrow|rbi\s+verification|police\s+uniform|skype(\s+video)?\s+call)\b',
            "weight": 75,
            "severity": "High",
            "title": "Digital Arrest & Law Enforcement Extortion",
            "desc": "Claims you are under 'Digital Arrest' or involved in illegal parcels. There is NO legal provision for 'Digital Arrest' in Indian law. Law enforcement NEVER interrogates or collects money via video calls."
        },
        {
            "category": "Fake Job & Part-Time Task Scam",
            "regex": r'\b(work\s+from\s+home|part[\-\s]time\s+job|earn\s+(\d{3,5})\s+(daily|per\s+day)|like\s+youtube\s+videos|hotel\s+rating|review\s+tasks|join\s+telegram|vip\s+task|prepaid\s+task|telegram\s+hr|ghar\s+baithe\s+kamaye|roj\s+(\d{3,5})\s+kamaye)\b',
            "weight": 55,
            "severity": "High",
            "title": "Work-From-Home / Telegram Task Scam",
            "desc": "Promises high daily earnings (₹2,000-₹5,000) for simple online tasks like liking videos, leading victims into advance payment traps via Telegram groups."
        },
        {
            "category": "Urgent KYC / Account Suspension",
            "regex": r'\b(kyc\s+update|kyc\s+expired|account\s+(blocked|suspended|deactivated)|pan\s+card\s+link|sim\s+block|sim\s+deactivated|within\s+24\s+hours|turant\s+update\s+kare|khata\s+block|sim\s+band|24\s+ghante\s+ke\s+andar)\b',
            "weight": 50,
            "severity": "High",
            "title": "Urgent KYC Expiration / Account Block Threat",
            "desc": "Fabricates urgent account suspension or SIM deactivation to induce panic and force victims into clicking malicious links."
        },
        {
            "category": "Lottery & Prize Advance-Fee Fraud",
            "regex": r'\b(congratulations.*(won|winner)|kbc\s+lucky\s+draw|lottery\s+winner|won\s+₹?\d{5,8}|claim\s+your\s+prize|car\s+winner|free\s+gift\s+voucher|lucky\s+draw\s+me\s+naam|crorepati|इनाम|लॉटरी)\b',
            "weight": 60,
            "severity": "High",
            "title": "Fake Lottery / KBC Prize Claim",
            "desc": "Announces unsolicited lottery prizes or lucky draws, designed to extract 'registration fees', 'processing charges', or taxes before running away."
        },
        {
            "category": "UPI Social Engineering / Reverse Payment Trap",
            "regex": r'\b(scan\s+(this\s+)?qr(\s+code)?\s+to\s+receive|enter\s+upi\s+pin\s+to\s+receive|receive\s+money\s+via\s+qr|accept\s+payment\s+enter\s+pin|paise\s+pane\s+ke\s+liye\s+scan|pin\s+daal\s+kar\s+paise\s+le)\b',
            "weight": 65,
            "severity": "High",
            "title": "UPI 'Scan to Receive' Reverse Payment Trap",
            "desc": "Instructs you to scan a QR code or enter a UPI PIN to 'receive' funds. In UPI architecture, entering a PIN ALWAYS deducts money, never credits money!"
        },
        {
            "category": "Remote Access & Unknown APK Installation",
            "regex": r'\b(anysdesk|anydesk|quicksupport|teamviewer|rustdesk|screen\s+share|install\s+(unknown\s+)?apk|\.apk\b|download\s+app\s+via\s+link|download\s+support\s+app|app\s+install\s+kare)\b',
            "weight": 65,
            "severity": "High",
            "title": "Remote Access Tool / Malicious APK Request",
            "desc": "Instructs the recipient to install remote screen sharing tools (AnyDesk, QuickSupport) or sideload unverified .apk packages. Attackers use these to view OTPs and take over banking sessions."
        },
        {
            "category": "Fake Customer Care & Helpline Impersonation",
            "regex": r'\b(customer\s+care(\s+helpline)?|call\s+(official\s+)?care|toll[\-\s]free\s+support|swiggy\s+refund|zomato\s+refund|wallet\s+support|contact\s+helpline\s+\d{10})\b',
            "weight": 35,
            "severity": "Medium",
            "title": "Suspicious Customer Care Helpline Claim",
            "desc": "Claims to be customer care support offering refunds or helpline numbers. Scammers post fake numbers on search engines and chat messages to intercept troubled customers."
        },
        {
            "category": "Investment & High Return Ponzi Scheme",
            "regex": r'\b(guaranteed\s+returns?|double\s+your\s+money|100%\s+risk\s+free|daily\s+profit\s+guaranteed|crypto\s+doubler|forex\s+trading\s+signals\s+vip|paisa\s+double|bina\s+kisi\s+risk)\b',
            "weight": 40,
            "severity": "Medium",
            "title": "Unrealistic Guaranteed Investment Promise",
            "desc": "Promises guaranteed or doubled returns in short timeframes with zero risk, classic indicators of Ponzi schemes and unregulated crypto traps."
        },
        {
            "category": "Artificial Urgency & Pressure Tactics",
            "regex": r'\b(immediate(ly)?|urgent(ly)?|last\s+chance|final\s+notice|action\s+will\s+be\s+taken|legal\s+action|arrest\s+warrant|deadline(\s+tonight)?|tonight|turant|jaldi(\s+kare)?|asap)\b',
            "weight": 20,
            "severity": "Medium",
            "title": "High Psychological Urgency & Pressure",
            "desc": "Employs high-pressure coercive language to bypass rational thinking and rush the victim into impulsive compliance."
        },
        {
            "category": "Suspicious External Links in Message",
            "regex": r'https?://[^\s]+|bit\.ly/[^\s]+|t\.me/[^\s]+|wa\.me/[^\s]+|tinyurl\.com/[^\s]+|\.xyz[^\s]*|\.top[^\s]*',
            "weight": 20,
            "severity": "Medium",
            "title": "Unverified Hyperlink or Messaging Redirect",
            "desc": "Contains an external web link or instant messaging invite (Telegram/WhatsApp) redirecting conversations outside official verification channels."
        }
    ]

    @staticmethod
    def analyze(text: str) -> Dict[str, Any]:
        """
        Analyzes SMS, WhatsApp, Email, or Social Media messages for social engineering signals.
        Supports English, Hindi, and Hinglish.
        Extracts matched spans for rich frontend highlighting.
        """
        clean_text = (text or "").strip()
        if not clean_text:
            return {
                "risk_score": 0,
                "risk_level": "Low",
                "primary_category": "Empty Input",
                "indicators": [],
                "detected_indicators": [],
                "explanations": ["No text provided for analysis."],
                "recommendations": ["Please enter or paste a message to analyze."],
                "highlighted_spans": [],
                "scan_type": "message",
                "disclaimer": ""
            }

        risk_score = 0
        indicators = []
        highlighted_spans = []
        matched_categories = []

        lower_text = clean_text.lower()

        # Check each rule in the matrix
        for rule in MessageScanner.RULES:
            pattern = re.compile(rule["regex"], re.IGNORECASE)
            matches = list(pattern.finditer(clean_text))

            # Defensive negation check: distinguish between an OTP demand vs security advice ("Never share your OTP")
            if rule["category"] == "Credential & OTP Harvesting" and matches:
                threat_matches = []
                for m in matches:
                    prefix = clean_text[max(0, m.start() - 30):m.start()].lower()
                    suffix = clean_text[m.end():min(len(clean_text), m.end() + 30)].lower()
                    is_negated = any(neg in prefix for neg in ["do not", "never", "don't", "dont", "not", "kisi se", "mat", "na "]) or \
                                 any(neg in suffix for neg in ["na kare", "mat kare", "not allowed", "mat bataye", "mat batao", "is confidential"])
                    if not is_negated:
                        threat_matches.append(m)
                matches = threat_matches

            if matches:
                risk_score += rule["weight"]
                matched_categories.append(rule["category"])
                indicators.append({
                    "title": rule["title"],
                    "severity": rule["severity"],
                    "category": rule["category"],
                    "desc": rule["desc"]
                })

                # Record character span offsets for UI highlighting
                for m in matches:
                    highlighted_spans.append({
                        "start": m.start(),
                        "end": m.end(),
                        "text": clean_text[m.start():m.end()],
                        "category": rule["category"],
                        "severity": rule["severity"]
                    })

        # Check for presence of mobile phone numbers in text alongside action keywords
        phone_matches = re.findall(r'(\+?91[\-\s]?)?[6-9]\d{9}', clean_text)
        if phone_matches and ("call" in lower_text or "contact" in lower_text or "sampark" in lower_text):
            risk_score += 15
            indicators.append({
                "title": "Direct Mobile Number in Fraud Alert",
                "severity": "Medium",
                "category": "Suspicious Sender Callout",
                "desc": "Directs customer to an individual 10-digit mobile number rather than a verified toll-free or official banking IVR."
            })

        # Cap score at 100
        risk_score = min(100, max(0, risk_score))

        # Risk Classification
        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            if not indicators:
                indicators.append({
                    "title": "No Obvious Scam Signals Detected",
                    "severity": "Low",
                    "category": "Baseline",
                    "desc": "The text does not trigger known scam rules (OTP demands, digital arrest, fake job offers, APK downloads, or urgency coercion). Always verify identity before transferring funds."
                })

        # Primary Category Determination
        primary_category = matched_categories[0] if matched_categories else ("Clean / Low Risk" if risk_level == "Low" else "Unclassified Suspicion")

        # Explanations
        explanations = [f"{ind['title']}: {ind['desc']}" for ind in indicators]

        # Context-aware Safety Recommendations
        recommendations = MessageScanner.generate_recommendations(risk_level, matched_categories)

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "primary_category": primary_category,
            "indicators": indicators,
            "detected_indicators": [ind["title"] for ind in indicators],
            "explanations": explanations,
            "recommendations": recommendations,
            "highlighted_spans": highlighted_spans,
            "scan_type": "message",
            "disclaimer": "This score is an automated estimation based on linguistic and social engineering heuristics. It is not an absolute warranty. Do not label a message safe merely because no flags were raised."
        }

    @staticmethod
    def generate_recommendations(risk_level: str, categories: List[str]) -> List[str]:
        recs = []
        if "Credential & OTP Harvesting" in categories:
            recs.append("NEVER share your OTP, PIN, password, or CVV with anyone — banks and government agencies never ask for them.")
        if "UPI Social Engineering / Reverse Payment Trap" in categories:
            recs.append("CRITICAL: You never need to enter your UPI PIN or scan a QR code to RECEIVE money. Entering your PIN transfers funds out.")
        if "Digital Arrest / Law Enforcement Impersonation" in categories:
            recs.append("There is NO legal concept of 'Digital Arrest' in India. Police or CBI will never interrogate or accept bail money over WhatsApp or Skype.")
        if "Remote Access & Unknown APK Installation" in categories:
            recs.append("NEVER install AnyDesk, QuickSupport, TeamViewer, or sideload APK files sent by strangers. Doing so gives attackers control of your screen and OTPs.")
        if "Urgent Utility / Electricity Power Cut" in categories:
            recs.append("Verify power bills solely on your electricity board's verified official portal or app, not via phone numbers sent in SMS.")
        if "Fake Job & Part-Time Task Scam" in categories:
            recs.append("Refuse any job demanding advance registration fees or cryptocurrency deposits. Legitimate companies never pay employees via Telegram tasks.")
        if "Fake Customer Care & Helpline Impersonation" in categories:
            recs.append("Do NOT search for customer service phone numbers on Google or social media. Look for support numbers inside the verified official app.")

        # General guidance
        if risk_level == "High":
            recs.append("Block and report the sender immediately in your messaging application.")
            recs.append("Report financial cyber fraud immediately to National Cyber Crime Reporting Portal at https://cybercrime.gov.in or dial National Helpline 1930.")
        elif risk_level == "Medium":
            recs.append("Do not click any embedded links or call the contact number provided in this message.")
            recs.append("Verify sender identity through independently obtained official customer service channels.")
        else:
            recs.append("Always exercise caution if an unexpected message asks you to download apps, share data, or send money.")

        return recs


# =====================================================================
# AI EXPLAINER (OFFLINE FIRST EXPLAINABILITY)
# =====================================================================

class AIExplainer:
    @staticmethod
    def generate_ai_explanation(scan_type: str, content: str, analysis_result: Dict[str, Any], api_key: str = None) -> str:
        """
        Provides enhanced narrative explanation.
        Runs 100% offline without requiring paid APIs.
        Synthesizes how the score was calculated and why content may be dangerous.
        """
        risk = analysis_result.get("risk_level", "Unknown")
        score = analysis_result.get("risk_score", 0)
        category = analysis_result.get("primary_category", "General")
        indicators = analysis_result.get("indicators", [])

        reasons = [f"• {ind['title']}: {ind['desc']}" for ind in indicators[:3]]
        reasons_text = "\n".join(reasons) if reasons else "• No overt social engineering or malicious patterns matched."

        explanation = (
            f"ScamShield AI scored this {scan_type.upper()} at {score}/100 ({risk} Risk) under the category '{category}'.\n\n"
            f"Key observations:\n{reasons_text}\n\n"
            f"Our heuristic engine emphasizes defense-in-depth: attackers exploit urgency, impersonation, and misleading links. "
            f"Always rely on verified direct channels."
        )
        return explanation


# =====================================================================
# UNIFIED CONVENIENCE DETECTOR
# =====================================================================

def detect_scam(content: str, content_type: str = "auto") -> Dict[str, Any]:
    """
    Unified entry point for both URL and message scanning.
    If content_type == 'auto', dynamically determines whether content is a URL or message.
    """
    cleaned = (content or "").strip()
    if not cleaned:
        return {
            "risk_score": 0,
            "risk_level": "Low",
            "primary_category": "Empty Input",
            "indicators": [],
            "detected_indicators": [],
            "explanations": ["Input was empty."],
            "recommendations": ["Please enter a URL or message to analyze."],
            "scan_type": "unknown",
            "disclaimer": "Automated preliminary heuristic assessment."
        }

    # Determine type if auto
    actual_type = content_type.lower()
    if actual_type == "auto":
        # If it looks like a URL (starts with http:// or https:// or has no spaces and contains common TLD / domain syntax)
        is_url_like = bool(re.match(r'^(https?://|[a-zA-Z0-9-]+\.[a-zA-Z]{2,})[^\s]*$', cleaned))
        if is_url_like and len(cleaned.split()) == 1:
            actual_type = "url"
        else:
            actual_type = "message"

    if actual_type == "url":
        result = URLScanner.analyze(cleaned)
    else:
        result = MessageScanner.analyze(cleaned)

    result["summary"] = AIExplainer.generate_ai_explanation(result.get("scan_type", actual_type), cleaned, result)
    return result
