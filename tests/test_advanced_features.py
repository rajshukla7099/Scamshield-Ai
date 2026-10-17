"""
ScamShield AI - Tests for Deepfake, Threat Radar, and Incident FIR Generator
"""

import unittest
from detection.deepfake import DeepfakeDetector
from detection.threat_radar import ThreatRadar
from detection.incident_dossier import IncidentDossierGenerator
from detection.news_service import CyberNewsService
from detection.chatbot_engine import ShieldBotEngine
from app import app

class TestDeepfakeDetector(unittest.TestCase):
    def test_digital_arrest_detection(self):
        text = "Caller from CBI claimed my FedEx parcel had narcotics and put me under digital arrest on Skype video. Transfer to secret RBI verification account."
        res = DeepfakeDetector.analyze(text, "video")
        self.assertGreaterEqual(res["risk_score"], 65)
        self.assertEqual(res["risk_level"], "High")
        self.assertTrue(res["is_deepfake_likely"])
        self.assertTrue(any("Digital Arrest" in ind["title"] or "Impersonation" in ind["title"] for ind in res["indicators"]))

    def test_voice_cloning_detection(self):
        text = "Dad please help me, I am at the police station after a car accident. Send money immediately to my friend's account, don't tell mom."
        res = DeepfakeDetector.analyze(text, "voice")
        self.assertGreaterEqual(res["risk_score"], 60)
        self.assertEqual(res["risk_level"], "High")

    def test_clean_conversation(self):
        text = "Hello, this is your bank branch calling to invite you for your annual locker agreement renewal in person at the branch."
        res = DeepfakeDetector.analyze(text, "voice")
        self.assertLess(res["risk_score"], 35)
        self.assertEqual(res["risk_level"], "Low")
        self.assertFalse(res["is_deepfake_likely"])

class TestThreatRadar(unittest.TestCase):
    def test_sqli_detection(self):
        payload = "' OR '1'='1' --"
        res = ThreatRadar.analyze_payload(payload)
        self.assertGreaterEqual(res["risk_score"], 50)
        self.assertTrue(res["is_malicious"])
        self.assertIn("SQL Injection", res["matched_categories"])

    def test_sqli_union(self):
        payload = "' UNION ALL SELECT null, username, password FROM users --"
        res = ThreatRadar.analyze_payload(payload)
        self.assertGreaterEqual(res["risk_score"], 50)
        self.assertIn("SQL Injection", res["matched_categories"])

    def test_xss_detection(self):
        payload = "<script>alert(document.cookie)</script>"
        res = ThreatRadar.analyze_payload(payload)
        self.assertGreaterEqual(res["risk_score"], 50)
        self.assertIn("Cross-Site Scripting (XSS)", res["matched_categories"])

    def test_malware_apk(self):
        payload = "http://sbi-verification.xyz/downloads/sbi_security_update.apk"
        res = ThreatRadar.analyze_payload(payload)
        self.assertGreaterEqual(res["risk_score"], 40)
        self.assertIn("Malware & Ransomware", res["matched_categories"])

    def test_clean_input(self):
        payload = "search?q=laptop+bags&filter=price_asc"
        res = ThreatRadar.analyze_payload(payload)
        self.assertLess(res["risk_score"], 30)
        self.assertFalse(res["is_malicious"])

class TestIncidentDossierGenerator(unittest.TestCase):
    def test_dossier_generation(self):
        data = {
            "victim_name": "Test User",
            "victim_phone": "+91 9876543210",
            "victim_city": "Jaipur",
            "bank_name": "sbi",
            "loss_amount": "25000",
            "transaction_id": "SBI12345678",
            "scam_type": "Electricity Bill Scam",
            "suspect_info": "+91 9988776655",
            "description": "Installed fake APK and lost Rs 25000"
        }
        dossier = IncidentDossierGenerator.generate_dossier(data)
        self.assertTrue(dossier["success"])
        self.assertIn("action_plan", dossier)
        self.assertIn("police_fir", dossier)
        self.assertIn("bank_dispute", dossier)
        self.assertIn("portal_prompt", dossier)
        self.assertIn("Test User", dossier["police_fir"])
        self.assertIn("25000", dossier["police_fir"])
        self.assertIn("State Bank of India", dossier["bank_dispute"])
        self.assertIn("DBR.No.Leg.BC.78", dossier["bank_dispute"])

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_new_pages(self):
        self.assertEqual(self.client.get("/deepfake-checker").status_code, 200)
        self.assertEqual(self.client.get("/threat-radar").status_code, 200)
        self.assertEqual(self.client.get("/fir-generator").status_code, 200)

    def test_deepfake_api(self):
        res = self.client.post("/api/scan/deepfake", json={"text": "CBI Digital Arrest on Skype transfer to RBI"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

    def test_payload_api(self):
        res = self.client.post("/api/scan/payload", json={"payload": "' OR 1=1 --"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

    def test_incident_api(self):
        res = self.client.post("/api/incident/generate", json={
            "victim_name": "Raj",
            "loss_amount": "10000",
            "bank_name": "hdfc"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

    def test_news_page(self):
        res = self.client.get("/news")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Cyber Attack Intelligence", res.data)

    def test_news_api(self):
        res = self.client.get("/api/news?category=banking")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreater(len(data["news"]), 0)

    def test_chat_api(self):
        res = self.client.post("/api/chat", json={"message": "Mere paise cut gaye kya karu"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("1930", data["response"]["reply"])

class TestCyberNewsService(unittest.TestCase):
    def test_get_all_news(self):
        items = CyberNewsService.get_news("all")
        self.assertGreaterEqual(len(items), 5)
        for item in items:
            self.assertIn("title", item)
            self.assertIn("summary", item)
            self.assertIn("severity", item)

    def test_filter_category(self):
        items = CyberNewsService.get_news("Ransomware")
        self.assertTrue(all(item["category"] == "Ransomware" for item in items))
        self.assertGreaterEqual(len(items), 1)

class TestShieldBotEngine(unittest.TestCase):
    def test_financial_fraud_response(self):
        res = ShieldBotEngine.get_response("Account se 50000 rupees debit ho gaye fraud me")
        self.assertIn("1930", res["reply"])
        self.assertIn("Golden Hour", res["reply"])

    def test_digital_arrest_response(self):
        res = ShieldBotEngine.get_response("CBI police video call digital arrest warrant bol rhe hai")
        self.assertIn("FAKE", res["reply"])
        self.assertIn("Digital Arrest", res["title"])

    def test_upi_trap_response(self):
        res = ShieldBotEngine.get_response("OLX buyer bol rha hai QR code scan karke PIN daalo to paise aayenge")
        self.assertIn("PIN", res["reply"])

    def test_default_greeting(self):
        res = ShieldBotEngine.get_response("hello there")
        self.assertIn("ShieldBot AI", res["title"])

if __name__ == "__main__":
    unittest.main()

