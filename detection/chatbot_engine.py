"""
ScamShield AI - ShieldBot Intelligent Cyber Assistant Engine
Provides 24/7 emergency incident guidance, scam deconstruction,
and legal FIR advice in Hindi, Hinglish, and English.
"""

import re
from typing import Dict, Any, List

class ShieldBotEngine:
    """
    Intelligent chatbot engine answering cyber attack queries, financial fraud emergencies,
    and technical defense questions without external API costs.
    """

    INTENT_RESPONSES = [
        # 1. Financial Fraud / Money Deducted Emergency
        {
            "patterns": [
                r"\b(paise|rupaye|rupee|rupees|money|amount|paisa|cash|fund|rs|inr)\b.*\b(cut|kat|debit|debited|deducted|stolen|fraud|chala gaya|nikal gaye|gaya)\b",
                r"\b(cut|kat|debit|debited|deducted|stolen|fraud|chala gaya|nikal gaye|lost|loss)\b.*\b(paise|rupaye|rupee|rupees|money|amount|paisa|cash|fund|rs|inr)\b",
                r"\b(unauthorized|fraudulent|unknown).*(transaction|debit|transfer|withdrawal|payment)\b",
                r"\b(mere paise|paise cut|paisa kat|account se|lost money|scammed me|fraud hua)\b"
            ],
            "title": "🚨 Emergency Financial Fraud Recovery Protocol",
            "reply": (
                "🚨 **Ghabraye nahi, immediate ye 3 steps follow karein:**\n\n"
                "1. **Dial 1930 Immediately (Golden Hour):** National Cyber Crime Helpline '1930' par call karein aur transaction UTR batayein. Ye beneficiary bank me paiso ko cash nikalne se pehle freeze karwa sakte hain.\n"
                "2. **Bank Card & NetBanking Block:** Turant apne bank ke customer care par call karke card/UPI ko block karein.\n"
                "3. **File FIR & Bank Dispute:** Hamare platform par **[FIR & Recovery Dossier Generator](/fir-generator)** use karein. Isse aapko Police FIR application aur RBI Zero-Liability bank claim letter ready mil jayega.\n\n"
                "Official Portal: [cybercrime.gov.in](https://cybercrime.gov.in)"
            ),
            "quick_actions": [
                {"label": "🚨 Generate Police FIR & Bank Letter", "url": "/fir-generator"},
                {"label": "📞 Helpline Numbers", "action": "show_helplines"}
            ]
        },

        # 2. Digital Arrest / Police / CBI Video Call
        {
            "patterns": [
                r"\b(digital arrest|cbi|ed|narcotics|police|customs|crime branch|skype|parcel.*drugs)\b",
                r"\b(arrest warrant|supreme court|court order|rbi verification account)\b",
                r"\b(cbi call|police video call|arrest bol rhe hai)\b"
            ],
            "title": "⚖️ Fake Police / CBI 'Digital Arrest' Warning",
            "reply": (
                "⚠️ **YE 100% FAKE SCAM HAI! AAP BILKUL SAFE HAIN.**\n\n"
                "• **Indian Law Fact:** Indian Police, CBI, ED ya Customs **KABHI BHI** Skype, WhatsApp video call par interrogation nahi karte aur na hi 'Digital Arrest' jaisa koi legal provision hai.\n"
                "• **Fake Uniform & Backdrop:** Scammers fake police uniform aur CBI logo lagakar darate hain taaki aap paise transfer karein.\n"
                "• **Never Pay RBI Account:** RBI ka koi citizen verification account nahi hota. **Call turant disconnect karein** aur number ko block karein.\n\n"
                "Iski report aap hamare **[Deepfake & Impersonation Checker](/deepfake-checker)** par inspect kar sakte hain."
            ),
            "quick_actions": [
                {"label": "🎭 Check in Deepfake Radar", "url": "/deepfake-checker"},
                {"label": "🚨 File Incident FIR", "url": "/fir-generator?type=Digital%20Arrest%20Scam"}
            ]
        },

        # 3. UPI QR Code / Scan to Receive Scam
        {
            "patterns": [
                r"\b(qr code|scan.*receive|upi.*receive|paise lene k liye|enter upi pin|pin maang)\b",
                r"\b(olx|quikr|advance token|army officer.*olx)\b"
            ],
            "title": "📲 UPI 'Scan to Receive' Reverse Fraud Trap",
            "reply": (
                "🛑 **ALERT: PAISA RECEIVE KARNE KE LIYE KABHI BHI UPI PIN NAHI DAALNA HOTA!**\n\n"
                "• **Golden Rule of UPI:** UPI PIN sirf tab lagta hai jab aapke account se **PAISE KAT'TE (DEBIT)** hote hain. Kisi se paise lene (CREDIT) ke liye koi PIN ya QR scan nahi karna padta.\n"
                "• Scammers QR code bhej kar bolte hain 'Scan karo aur PIN daalo token money mil jayega'. Jaise hi aap PIN daalte hain, paise unke paas chale jate hain.\n"
                "• Is sender ko turant block karein aur kisi bhi QR code par PIN enter na karein."
            ),
            "quick_actions": [
                {"label": "🔍 Inspect Link or Message", "url": "/"}
            ]
        },

        # 4. Electricity Bill / Power Cut Scam
        {
            "patterns": [
                r"\b(electricity|power.*cut|bijli.*kat|unpaid bill|light kat jayegi|officer.*call)\b",
                r"\b(bijli bill|power disconnection)\b"
            ],
            "title": "⚡ Fake Electricity Bill Disconnection Scam",
            "reply": (
                "⚠️ **Caution: Fake Electricity Board Threat!**\n\n"
                "• Electricity department kabhi bhi personal 10-digit mobile number se SMS bhej kar nahi kehti ki 'aaj raat 9:30 baje bijli kat jayegi'.\n"
                "• SMS me diye gaye number par call mat karein. Wo aapse **AnyDesk, QuickSupport ya Fake APK** install karwa kar aapka bank account khali kar denge.\n"
                "• Hamesha official bijli board app ya website se bill check karein."
            ),
            "quick_actions": [
                {"label": "🔍 Scan SMS Message", "url": "/analyzer"}
            ]
        },

        # 5. Telegram / WFH Job Scam
        {
            "patterns": [
                r"\b(telegram|part time|wfh|work from home|job offer|like youtube|rating.*task|daily 5000)\b",
                r"\b(ghar baithe|crypto task|prepaid task)\b"
            ],
            "title": "💼 Fake Telegram Part-Time Job Scam",
            "reply": (
                "🚫 **Ye Fraud Hai!**\n\n"
                "• Shuru me wo aapko YouTube video like karne ke 150-300 rupaye dekar bharosa jeet'te hain.\n"
                "• Uske baad Telegram VIP group me add karke 'Crypto Investment' ya 'Prepaid Task' ke naam par 50,000 se 5 lakh rupaye maangte hain aur withdraw nahi karne dete.\n"
                "• Koi bhi real company salary dene ke liye aapse paise deposit nahi karwati. Turant exit karein!"
            ),
            "quick_actions": [
                {"label": "🔍 Scan Job Offer", "url": "/analyzer"}
            ]
        },

        # 6. Deepfake & Voice Cloning
        {
            "patterns": [
                r"\b(voice clone|cloning|deepfake|awaz.*accident|bachhe ki awaz|hospital.*emergency)\b",
                r"\b(relative voice|son voice|daughter voice)\b"
            ],
            "title": "🎭 AI Voice Cloning Emergency Extortion",
            "reply": (
                "⚠️ **AI Voice Cloning Warning:**\n\n"
                "• Aaj kal AI technology se sirf 3-second ke voice sample se kisi ki bhi aawaz banayi ja sakti hai.\n"
                "• Agar koi beta/beti ya relative ban kar hospital accident ya police bail ke liye urgent paise maange:\n"
                "  1. Call turant kaat kar unke **regular phone number par direct call karein**.\n"
                "  2. Apne family me ek **Family Safe Word** rakhein jo sirf aapke ghar walo ko pata ho."
            ),
            "quick_actions": [
                {"label": "🎭 Deepfake Forensic Radar", "url": "/deepfake-checker"}
            ]
        },

        # 7. Web & Cyber Attack Inquiries (SQLi, XSS, DDoS, Malware)
        {
            "patterns": [
                r"\b(sqli|sql injection|xss|cross site|ddos|dos|brute force|malware|ransomware|mitm)\b",
                r"\b(attack|vulnerability|payload|exploit)\b"
            ],
            "title": "🛡️ Cyber Attack & Vulnerability Defense",
            "reply": (
                "🛡️ **Technical Cyber Defense Analysis:**\n\n"
                "Hamare platform me dedicated **[Cyber Threat & Attack Radar](/threat-radar)** engine shamil hai jo:\n"
                "• **SQL Injection (SQLi):** Parameterized queries aur ORM enforcement detect karta hai.\n"
                "• **XSS (Cross-Site Scripting):** Dynamic input sanitization aur CSP rules analyze karta hai.\n"
                "• **Malware & Ransomware APKs:** Malicious payload extensions aur ransom notes pakadta hai.\n"
                "• **DDoS & Brute-Force:** Rate limiting anomalies aur credential stuffing identify karta hai."
            ),
            "quick_actions": [
                {"label": "⚡ Open Cyber Threat Radar", "url": "/threat-radar"}
            ]
        }
    ]

    DEFAULT_RESPONSE = {
        "title": "🛡️ ShieldBot AI Cyber Assistant",
        "reply": (
            "Namaste! Main **ShieldBot AI** hoon — aapka 24/7 Digital Safety Assistant.\n\n"
            "Main aapki in mamlo me madad kar sakta hoon:\n"
            "• **Paise cut gaye?** 1930 helpline aur instant bank recovery plan\n"
            "• **CBI / Police video call?** Digital Arrest scam verification\n"
            "• **UPI ya OLX fraud?** Reverse QR payment traps se bachav\n"
            "• **Suspicious link ya SMS?** Real-time safety analysis\n"
            "• **Legal FIR:** Ready-to-submit police complaint letter\n\n"
            "Aap apna sawal Hindi, English ya Hinglish me type kar sakte hain!"
        ),
        "quick_actions": [
            {"label": "🚨 Paise cut gaye kya karu?", "query": "Mere paise cut gaye kya karu"},
            {"label": "⚖️ CBI Video Call Digital Arrest", "query": "CBI police video call digital arrest"},
            {"label": "📲 UPI QR Code Scan Scam", "query": "UPI scan karke paise lene ka scam"},
            {"label": "⚡ Electricity Bill Cut Message", "query": "Bijli bill cut hone ka message aaya"}
        ]
    }

    @classmethod
    def get_response(cls, user_message: str) -> Dict[str, Any]:
        """
        Processes user query and returns structured safety response.
        """
        cleaned = (user_message or "").strip().lower()
        if not cleaned:
            return cls.DEFAULT_RESPONSE

        for item in cls.INTENT_RESPONSES:
            for pattern in item["patterns"]:
                if re.search(pattern, cleaned, re.IGNORECASE):
                    return {
                        "title": item["title"],
                        "reply": item["reply"],
                        "quick_actions": item.get("quick_actions", [])
                    }

        # Check if user passed a URL directly
        if re.search(r'https?://[^\s]+', cleaned) or re.search(r'\b[a-zA-Z0-9-]+\.(com|in|xyz|top|org|net|co)\b', cleaned):
            return {
                "title": "🔗 URL Detected in Conversation",
                "reply": (
                    "Maine aapke message me ek link identify kiya hai. Kisi bhi anjaan link par click karne se pehle "
                    "hamaare **[URL Scanner](/)** par paste karke check karein. Ye typosquatting, credential theft aur malicious TLDs ko bina link khole offline inspect karta hai."
                ),
                "quick_actions": [
                    {"label": "🔗 Open URL Scanner", "url": "/scanner"}
                ]
            }

        return cls.DEFAULT_RESPONSE
