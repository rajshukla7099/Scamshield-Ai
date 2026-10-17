import json
from database import init_db, get_db_connection

def seed_database():
    """Seeds the database with realistic initial scans, reports, and educational scenarios."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) as cnt FROM quizzes")
    if cursor.fetchone()["cnt"] > 0:
        conn.close()
        return

    # Seed Quizzes
    quiz_data = [
        (
            "Digital Arrest / CBI Impersonation",
            "Urgent: You received a video call on Skype from a person in police uniform claiming you are under 'Digital Arrest' for an illegal FedEx parcel containing narcotics sent to Thailand in your name. They demand you transfer ₹2,50,000 into a 'RBI Verification Escrow Account' to prove innocence.",
            "Video Call / WhatsApp",
            1,
            "Intermediate",
            "Digital Arrest & Legal Impersonation",
            "Indian law enforcement agencies (Police, CBI, ED, Narcotics) NEVER conduct 'Digital Arrests' over Skype, WhatsApp, or video calls. Neither the Reserve Bank of India nor law enforcement maintains personal escrow accounts to clear suspects. This is a severe cyber extortion scam.",
            json.dumps([
                "No such legal concept as 'Digital Arrest' exists under Indian Law",
                "Police/CBI never interrogate or mandate bail deposits via WhatsApp/Skype",
                "High psychological coercion and immediate financial transfer demand",
                "Legitimate police summons are issued physically with valid warrants"
            ])
        ),
        (
            "Urgent Electricity Disconnection Threat",
            "Dear Consumer, Your Electricity power connection will be disconnected tonight at 9:30 PM from the power sub-station because your previous month bill was not updated. Immediately contact our electricity officer Rahul Sharma at 9876543210 to avoid blackout.",
            "SMS",
            1,
            "Beginner",
            "Utility & Bill Scam",
            "State electricity boards (like BESCOM, MSEDCL, TPDDL, etc.) NEVER send personal mobile numbers for bill payments or threaten instant power cuts within hours via generic SMS. All bill alerts come from registered alphanumeric sender headers (e.g., JD-BESCOM).",
            json.dumps([
                "Sent from an unverified individual 10-digit mobile number",
                "Artificial panic with severe deadline ('tonight at 9:30 PM')",
                "Directs victim to call an individual rather than an official utility portal"
            ])
        ),
        (
            "Legitimate Bank Suspicious Activity Alert",
            "HDFC Bank Alert: An unusual debit card transaction of ₹4,999 on Amazon India was attempted. If this was NOT you, immediately lock your card via your NetBanking app or dial the 24x7 customer helpline number printed on the back of your card. Do not share OTP.",
            "SMS",
            0,
            "Intermediate",
            "Legitimate Security Alert",
            "This is a legitimate bank alert. Notice that it does NOT contain any suspicious link, does NOT ask you to click anything, does NOT request passwords or OTPs, and explicitly advises you to use your official banking app or the verified number physically printed on your card.",
            json.dumps([
                "No malicious hyperlinks or unknown URLs",
                "Explicitly instructs user to protect OTPs",
                "Recommends verified official channels (back of physical card)"
            ])
        ),
        (
            "Part-Time YouTube/Telegram Review Job",
            "Congratulations! We have selected your resume for Work From Home. Daily income: ₹2,000 - ₹5,000 for liking YouTube videos and rating Google Maps hotels. Only 2 hours daily. Click link to join our VIP HR Manager on Telegram: https://t.me/earn_daily_vip_jobs",
            "WhatsApp",
            1,
            "Beginner",
            "Fake Job Offer",
            "This is the notorious 'Task Scam'. Scammers pay tiny amounts (₹150-₹500) for the first 2 tasks to build trust, then trap victims into 'prepaid crypto trading tasks' requiring thousands of rupees to withdraw funds, leading to massive financial loss.",
            json.dumps([
                "Unrealistic high earnings (₹5,000/day) for trivial tasks (liking videos)",
                "Recruitment conducted entirely via anonymous Telegram groups",
                "No legitimate company hires or pays salaries through personal Telegram links"
            ])
        ),
        (
            "UPI QR Code 'Scan to Receive Money'",
            "Buyer on OLX: 'Sir, I have transferred ₹12,000 for your old laptop. Please scan this PhonePe QR code and enter your UPI PIN to accept the credit into your bank account.'",
            "WhatsApp / UPI",
            1,
            "Beginner",
            "UPI Reverse Payment Fraud",
            "GOLDEN RULE OF UPI: You NEVER need to enter your UPI PIN or scan a QR code to RECEIVE money! Entering your UPI PIN is solely and exclusively used to DEDUCT money from your bank account.",
            json.dumps([
                "Entering a UPI PIN ALWAYS transfers money OUT of your account",
                "Scanning a QR code is exclusively for making payments, never receiving funds",
                "Common social engineering tactic on second-hand marketplaces like OLX"
            ])
        ),
        (
            "India Post Address Incomplete Notification",
            "IndiaPost: Your package IND984214 could not be delivered due to incomplete street address. Please update your delivery address within 24 hours at http://indiapost-parcels-track.top/address otherwise the parcel will be returned to sender.",
            "SMS",
            1,
            "Advanced",
            "Smishing & Brand Impersonation",
            "India Post operates exclusively on official government domains (.gov.in or .in). The link uses a high-risk scam TLD '.top' and an unofficial domain. Visiting this phishing site prompts users to pay a small ₹25 're-delivery fee' while capturing credit card details.",
            json.dumps([
                "Suspicious domain (indiapost-parcels-track.top) instead of official indiapost.gov.in",
                "Creates urgency ('within 24 hours') to trigger impulsive compliance",
                "Credential harvesting phishing trap designed to steal payment card CVVs"
            ])
        )
    ]

    for q in quiz_data:
        cursor.execute("""
            INSERT INTO quizzes (title, scenario_text, source_type, is_scam, difficulty, category, explanation, red_flags_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, q)

    # Seed realistic Scan History
    scans_data = [
        (
            "url",
            "http://sbi-kyc-verification-portal.xyz/login",
            94,
            "High",
            "Banking Phishing",
            json.dumps([
                {"title": "High-Risk Top Level Domain", "severity": "High", "desc": "Domain uses '.xyz', frequently exploited for throwaway phishing portals."},
                {"title": "Brand Impersonation (State Bank of India)", "severity": "High", "desc": "Domain matches protected banking entity 'sbi' but is not hosted on official onlinesbi.sbi."},
                {"title": "Missing HTTPS / Insecure Connection", "severity": "High", "desc": "URL uses plain unencrypted HTTP for sensitive banking credentials."},
                {"title": "Credential Harvesting Path", "severity": "Medium", "desc": "Deep path contains sensitive keyword '/login'."}
            ]),
            json.dumps([
                "Do not open or enter any passwords, NetBanking IDs, or OTPs on this page.",
                "Official State Bank of India portal is exclusively: https://onlinesbi.sbi",
                "Report immediately to official cyber fraud portal https://cybercrime.gov.in or call 1930."
            ]),
            "High confidence brand spoofing attempt targeting State Bank of India customers."
        ),
        (
            "message",
            "Aapka Bijli connection aaj raat 9:30 baje kat diya jayega kyunki bill update nahi...",
            88,
            "High",
            "Utility & Bill Scam",
            json.dumps([
                {"title": "Power Cut / Disconnection Coercion", "severity": "High", "desc": "Detected urgent electricity disconnection threat in Hinglish."},
                {"title": "Impersonation of Utility Department", "severity": "High", "desc": "Purports to represent electricity authority without official sender header."},
                {"title": "Artificial Short Deadline", "severity": "Medium", "desc": "Demands immediate action tonight to force emotional compliance."}
            ]),
            json.dumps([
                "Do not call individual mobile numbers mentioned in utility SMS alerts.",
                "Verify your bill status directly on your official state electricity board app.",
                "Electricity boards never authorize disconnections via individual WhatsApp messages."
            ]),
            "Urgent utility disconnection social engineering attempt in Hinglish."
        ),
        (
            "url",
            "https://onlinesbi.sbi",
            0,
            "Low",
            "Legitimate Banking",
            json.dumps([
                {"title": "Official Brand Domain Match", "severity": "Low", "desc": "Verified official top-level domain registered to State Bank of India."},
                {"title": "Secure HTTPS Protocol", "severity": "Low", "desc": "Utilizes TLS/SSL encryption for data transmission."}
            ]),
            json.dumps([
                "Always verify the green lock or certificate details in your browser address bar.",
                "Bookmark official banking links to prevent typo navigation."
            ]),
            "Legitimate official web portal."
        ),
        (
            "message",
            "Congratulations! Your mobile number won ₹25,00,000 in KBC Lucky Draw 2025...",
            95,
            "High",
            "Lottery & Prize Scam",
            json.dumps([
                {"title": "Unsolicited Huge Lottery Claim", "severity": "High", "desc": "Promises 25 Lakh INR without any prior ticket purchase or contest entry."},
                {"title": "KBC Brand Impersonation", "severity": "High", "desc": "Impersonates Kaun Banega Crorepati television show."},
                {"title": "Advance Processing Fee Trap", "severity": "High", "desc": "Classic 419 advance-fee fraud asking for registration or GST fees."}
            ]),
            json.dumps([
                "You cannot win a lottery or contest you never purchased or entered.",
                "Never send money to claim any prize, car, or lottery.",
                "Block and report the sender number."
            ]),
            "Classic advance-fee lottery fraud impersonating national television show."
        ),
        (
            "url",
            "http://192.168.1.45/paytm-kyc/verify.html",
            92,
            "High",
            "IP-Host Phishing",
            json.dumps([
                {"title": "Raw IP Address as Host", "severity": "High", "desc": "Website uses a raw numerical IP address instead of a registered domain name."},
                {"title": "Brand Keyword in Path", "severity": "High", "desc": "Path includes 'paytm-kyc' attempting to mimic Paytm payment service."},
                {"title": "Unencrypted HTTP Protocol", "severity": "High", "desc": "Lacks SSL certificate."}
            ]),
            json.dumps([
                "Never visit raw IP address links received in SMS or messages.",
                "Paytm never hosts user verification on private or unverified IP addresses."
            ]),
            "Malicious raw IP host hosting spoofed Paytm KYC credential harvester."
        )
    ]

    for s in scans_data:
        cursor.execute("""
            INSERT INTO scans (scan_type, target_preview, risk_score, risk_level, primary_category, indicators_json, recommendations_json, full_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, s)

    # Seed realistic Community Reports
    reports_data = [
        (
            "phone",
            "+91 98******12",
            "Utility Scam",
            "Caller impersonated electricity officer claiming power cut at 9:30 PM and demanded payment via QuickSupport APK.",
            "High Risk - Known Disconnection Fraud",
            "Verified Scam",
            14
        ),
        (
            "url",
            "http://indiapost-parcels-track.top/address",
            "Delivery Smishing",
            "Phishing site asking for ₹25 redelivery fee to harvest credit card details under India Post branding.",
            "High Risk - Credential Harvesting",
            "Verified Scam",
            28
        ),
        (
            "message",
            "Dear customer your SIM KYC has expired. Call VIP Airtel officer at +91 91******44 immediately...",
            "SIM Swap / KYC",
            "SMS claiming SIM deactivation within 12 hours unless an APK file is downloaded.",
            "High Risk - SIM Swap",
            "Verified Scam",
            19
        ),
        (
            "phone",
            "+91 88******90",
            "Digital Arrest",
            "Caller claimed to be DCP Cyber Cell Mumbai threatening arrest over an illegal FedEx parcel containing drugs.",
            "Critical - Extortion Attempt",
            "Verified Scam",
            42
        ),
        (
            "url",
            "https://telegram-task-vip-bonus.xyz/daily-income",
            "Fake Job",
            "Website promoting Telegram channel where users pay ₹3,000 VIP fee to get paid YouTube tasks.",
            "High Risk - Task Scam",
            "In Review",
            9
        )
    ]

    for r in reports_data:
        import hashlib
        content_hash = hashlib.sha256(r[1].lower().encode('utf-8')).hexdigest()
        cursor.execute("""
            INSERT INTO reports (report_type, target_content, content_hash, category, description, risk_assessment, status, upvotes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r[0], r[1], content_hash, r[2], r[3], r[4], r[5], r[6]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_database()
    print("Database successfully initialized and seeded with realistic threat intelligence datasets!")
