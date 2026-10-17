"""
ScamShield AI - AI Cyber Incident FIR & Crisis Dossier Generator
Generates comprehensive legal complaints, bank dispute representations,
and immediate 60-minute crisis recovery protocols for cyber fraud victims in India.
"""

from datetime import datetime
from typing import Dict, Any

class IncidentDossierGenerator:
    """
    Generates actionable recovery blueprints, official Police FIR applications,
    and RBI-compliant bank dispute letters tailored to specific scam scenarios.
    """

    BANK_HELPLINES = {
        "sbi": {"name": "State Bank of India", "toll_free": "1800 11 2211 / 1800 425 3800", "sms_block": "SMS 'BLOCK <last 4 digits>' to 567676", "email": "customercare@sbi.co.in"},
        "hdfc": {"name": "HDFC Bank", "toll_free": "1800 1600 / 1800 266 4332", "sms_block": "NetBanking Card Control / 1800 1600", "email": "support@hdfcbank.com"},
        "icici": {"name": "ICICI Bank", "toll_free": "1800 120 7777 / 1800 1080", "sms_block": "SMS 'BLOCK <card>' to 5676766", "email": "customer.care@icicibank.com"},
        "axis": {"name": "Axis Bank", "toll_free": "1860 419 5555 / 1860 500 5555", "sms_block": "SMS 'BLOCK <card>' to 5676782", "email": "nodal.officer@axisbank.com"},
        "pnb": {"name": "Punjab National Bank", "toll_free": "1800 180 2222 / 1800 103 2222", "sms_block": "SMS 'HOT <account no>' to 5607040", "email": "care@pnb.co.in"},
        "paytm": {"name": "Paytm Payments Bank", "toll_free": "0120-4456456", "sms_block": "Paytm 24x7 Helpdesk", "email": "nodal@paytmbank.com"},
        "general": {"name": "Commercial Bank", "toll_free": "National Helpline 1930", "sms_block": "Call Bank Cust Care immediately", "email": "report@cybercrime.gov.in"}
    }

    @classmethod
    def generate_dossier(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a complete crisis recovery dossier including:
        1. Action Plan ('Kya-Kya Karna Chahiye')
        2. Police FIR Complaint Letter
        3. Bank Chargeback Dispute Letter
        4. National Cyber Crime Portal filing prompt
        """
        victim_name = data.get("victim_name") or "Aggrieved Citizen"
        victim_phone = data.get("victim_phone") or "Provided in FIR"
        victim_city = data.get("victim_city") or "India"
        bank_key = (data.get("bank_name") or "general").lower().strip()
        bank_info = cls.BANK_HELPLINES.get(bank_key, cls.BANK_HELPLINES["general"])
        
        loss_amount = data.get("loss_amount") or "0"
        tx_id = data.get("transaction_id") or "Pending Bank Statement"
        suspect_info = data.get("suspect_info") or "Unknown Cyber Criminal"
        scam_type = data.get("scam_type") or "Online Financial Cyber Fraud"
        incident_time = data.get("incident_date") or datetime.now().strftime("%d-%m-%Y %H:%M")
        description = data.get("description") or "Deceived into unauthorized electronic fund transfer through social engineering."

        # -------------------------------------------------------------
        # 1. Action Plan: Kya-Kya Karna Chahiye (Immediate Protocols)
        # -------------------------------------------------------------
        action_plan = [
            {
                "phase": "Phase 1: First 60 Minutes (Golden Hour Protocol)",
                "steps": [
                    f"🚨 Dial National Cyber Crime Helpline '1930' immediately. Explain that an unauthorized transaction of ₹{loss_amount} occurred (Tx ID: {tx_id}). They can trigger an emergency inter-bank lien to freeze the stolen funds at the receiver's bank before cash withdrawal.",
                    f"📞 Call your bank's 24x7 emergency helpline ({bank_info['name']}: {bank_info['toll_free']}). Demand immediate hotlisting of your Debit Card, UPI ID, and temporary NetBanking freeze.",
                    f"📲 Use SMS emergency card block: {bank_info['sms_block']}."
                ]
            },
            {
                "phase": "Phase 2: Formal Filing (Within 2 to 24 Hours)",
                "steps": [
                    "📋 Register an official complaint online at https://cybercrime.gov.in under 'Financial Fraud'. Paste the pre-formatted Portal Prompt generated below.",
                    "🏦 Submit the written Bank Dispute Letter (generated below) to your home branch manager within 72 hours to claim RBI Zero-Liability protection under Circular DBR.No.Leg.BC.78/09.07.005/2017-18.",
                    "🚔 Submit the formal Police FIR application (generated below) to your nearest Cyber Crime Police Station along with your bank statement highlighting the debit entry."
                ]
            },
            {
                "phase": "Phase 3: Digital Device & Identity Lockdown",
                "steps": [
                    "📱 If prompted to install any app (AnyDesk, TeamViewer, RustDesk, QuickSupport, APK), UNINSTALL IT IMMEDIATELY and factory reset your phone.",
                    "🔒 Change your UPI MPIN, ATM PIN, NetBanking passwords, and primary email password from a different, clean device.",
                    "💬 Enable 2-Step Verification on WhatsApp, Google, and your primary SIM carrier to prevent SIM-swap hijacking."
                ]
            }
        ]

        # -------------------------------------------------------------
        # 2. Formal Police FIR Complaint Letter
        # -------------------------------------------------------------
        police_fir = f"""TO,
THE STATION HOUSE OFFICER (SHO) / IN-CHARGE,
CYBER CRIME POLICE STATION,
{victim_city.upper()}, INDIA.

DATE: {datetime.now().strftime("%d-%B-%Y")}

SUBJECT: COMPLAINT UNDER SECTIONS 43, 66C, 66D OF THE INFORMATION TECHNOLOGY ACT, 2000 AND SECTIONS 419, 420 OF THE INDIAN PENAL CODE (IPC) / CORRESPONDING PROVISIONS OF BHARATIYA NYAYA SANHITA (BNS) REGARDING CYBER FRAUD OF RS. {loss_amount}/-

Respected Sir/Madam,

I, {victim_name}, residing in {victim_city}, contact number {victim_phone}, submit this formal complaint regarding a cyber fraud incident wherein I have been defrauded of a sum of Rs. {loss_amount}/- (Rupees {loss_amount} only) on {incident_time}.

1. INCIDENT BRIEF & MODUS OPERANDI:
The incident pertains to a "{scam_type}". 
Details: {description}

2. TRANSACTION & FINANCIAL PARTICULARS:
• Bank Name: {bank_info['name']}
• Defrauded Amount: Rs. {loss_amount}/-
• Transaction Reference / UTR Number: {tx_id}
• Incident Date & Time: {incident_time}

3. SUSPECT IDENTIFIERS & DIGITAL FOOTPRINT:
• Suspect Phone / UPI ID / URL: {suspect_info}
• Platform Utilized: WhatsApp / SMS / Phone Call / Fraudulent Link

4. STATUTORY VIOLATIONS:
The accused has committed deliberate offenses under:
a) Section 66C, Information Technology Act, 2000 (Identity Theft)
b) Section 66D, Information Technology Act, 2000 (Cheating by personation using computer resource)
c) Section 420 / 419, Indian Penal Code (Cheating and dishonestly inducing delivery of property)

5. PRAYER / RELIEF SOUGHT:
In light of the above facts, I respectfully request your office to:
1. Register an FIR under the appropriate provisions of law against the suspect(s).
2. Issue necessary notices to the beneficiary bank / nodal officer to freeze the fraudulent account holding Rs. {loss_amount}/-.
3. Trace the call logs, IP addresses, and KYC records associated with suspect {suspect_info}.

I am ready to provide all corroborating evidence including bank statements, call recordings, and screenshot logs to assist the investigation.

Yours faithfully,

(Signature)
Name: {victim_name}
Mobile: {victim_phone}
Address: {victim_city}
Enclosures: Bank Account Statement, Screenshot of Fraudulent Transaction, Call Logs.
"""

        # -------------------------------------------------------------
        # 3. Official Bank Dispute & Chargeback Letter
        # -------------------------------------------------------------
        bank_dispute = f"""TO,
THE BRANCH MANAGER / PRINCIPAL NODAL OFFICER,
{bank_info['name'].upper()},
{victim_city.upper()} BRANCH.

DATE: {datetime.now().strftime("%d-%B-%Y")}

SUBJECT: NOTICE OF UNAUTHORIZED ELECTRONIC TRANSACTION & CLAIM FOR REVERSAL UNDER RBI CIRCULAR DBR.No.Leg.BC.78/09.07.005/2017-18

Respected Sir/Madam,

Account Holder Name: {victim_name}
Registered Mobile: {victim_phone}
Bank Name: {bank_info['name']}

I am writing to formally report an unauthorized electronic fund transfer from my bank account, executed without my valid informed consent, on {incident_time}.

TRANSACTION DETAILS:
• Disputed Amount: Rs. {loss_amount}/-
• Transaction ID / UTR: {tx_id}
• Date & Time: {incident_time}
• Beneficiary / Suspect: {suspect_info}
• Scam Modus Operandi: {scam_type}

LEGAL POSITION & RBI MANDATE:
Under Reserve Bank of India Master Circular DBR.No.Leg.BC.78/09.07.005/2017-18 dated July 6, 2017 on "Customer Protection – Limiting Liability of Customers in Unauthorised Electronic Banking Transactions":
1. The customer liability is Zero where the unauthorized transaction occurs through third-party breach/fraud and the customer notifies the bank within 3 working days.
2. The bank is mandated to credit (shadow reversal) the disputed amount to the customer's account within 10 working days from the date of such notification.

I have notified your emergency desk and have also reported this incident to the National Cyber Crime Reporting Portal (Helpline 1930).

I formally request your branch to:
1. Immediately initiate an inter-bank recall / chargeback request with the beneficiary bank.
2. Provide provisional credit of Rs. {loss_amount}/- to my account in compliance with RBI guidelines.
3. Issue an official dispute acknowledgment number for my records.

Yours sincerely,

(Signature)
Name: {victim_name}
Phone: {victim_phone}
"""

        # -------------------------------------------------------------
        # 4. National Cyber Crime Portal (cybercrime.gov.in) Prompt
        # -------------------------------------------------------------
        portal_prompt = (
            f"On {incident_time}, I became a victim of a cyber fraud categorized as '{scam_type}'. "
            f"An unauthorized sum of Rs. {loss_amount}/- was debited from my {bank_info['name']} account "
            f"(Transaction ID / UTR: {tx_id}). "
            f"The suspect contacted me via '{suspect_info}'. "
            f"Brief details: {description}. "
            f"I have already informed my bank and request urgent fund tracing and freezing of the recipient account under Helpline 1930."
        )

        return {
            "success": True,
            "action_plan": action_plan,
            "police_fir": police_fir,
            "bank_dispute": bank_dispute,
            "portal_prompt": portal_prompt,
            "bank_info": bank_info,
            "summary": {
                "victim_name": victim_name,
                "loss_amount": loss_amount,
                "scam_type": scam_type,
                "tx_id": tx_id,
                "suspect_info": suspect_info
            }
        }
