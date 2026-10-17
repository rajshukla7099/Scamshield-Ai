import unittest
from detector import URLScanner, MessageScanner, calculate_entropy, levenshtein_distance

class TestURLScanner(unittest.TestCase):
    def test_https_check(self):
        result = URLScanner.analyze("http://example-login.com")
        self.assertGreaterEqual(result["risk_score"], 20)
        self.assertTrue(any("HTTP" in ind["title"] for ind in result["indicators"]))

    def test_ip_address_host(self):
        result = URLScanner.analyze("http://192.168.1.100/sbi/login.html")
        self.assertGreaterEqual(result["risk_score"], 70)
        self.assertEqual(result["risk_level"], "High")
        self.assertTrue(any("IP Address" in ind["title"] for ind in result["indicators"]))

    def test_high_risk_tld(self):
        result = URLScanner.analyze("https://secure-banking-verify.xyz")
        self.assertGreaterEqual(result["risk_score"], 30)
        self.assertTrue(any(".xyz" in ind["title"] for ind in result["indicators"]))

    def test_url_shortener(self):
        result = URLScanner.analyze("https://bit.ly/free-prize-bonus")
        self.assertGreaterEqual(result["risk_score"], 25)
        self.assertTrue(any("Shortener" in ind["title"] for ind in result["indicators"]))

    def test_brand_impersonation(self):
        result = URLScanner.analyze("http://sbi-kyc-verification-portal.xyz/login")
        self.assertGreaterEqual(result["risk_score"], 80)
        self.assertEqual(result["risk_level"], "High")
        self.assertTrue(any("State Bank of India" in ind["title"] for ind in result["indicators"]))

    def test_typosquatting(self):
        result = URLScanner.analyze("https://g00gle.com")
        self.assertGreaterEqual(result["risk_score"], 30)

    def test_legitimate_url(self):
        result = URLScanner.analyze("https://onlinesbi.sbi")
        self.assertLess(result["risk_score"], 30)
        self.assertEqual(result["risk_level"], "Low")

    def test_malformed_url_safety(self):
        # Must not raise exceptions or crash
        result = URLScanner.analyze("not a valid :// url ???")
        self.assertIn("risk_score", result)


class TestMessageScanner(unittest.TestCase):
    def test_otp_pin_harvesting(self):
        msg = "Dear customer, your bank requires you to share your OTP and enter UPI PIN immediately."
        res = MessageScanner.analyze(msg)
        self.assertGreaterEqual(res["risk_score"], 60)
        self.assertTrue(any("OTP" in ind["title"] for ind in res["indicators"]))

    def test_hinglish_electricity_cut(self):
        msg = "Dear Consumer, Aapka bijli connection aaj raat 9:30 baje kat diya jayega turant contact electricity officer Rahul."
        res = MessageScanner.analyze(msg)
        self.assertGreaterEqual(res["risk_score"], 50)
        self.assertTrue(any("Electricity" in ind["title"] for ind in res["indicators"]))

    def test_digital_arrest_extortion(self):
        msg = "CBI cyber crime cell notice: you are under digital arrest for illegal drugs parcel sent to Thailand. Join Skype call."
        res = MessageScanner.analyze(msg)
        self.assertGreaterEqual(res["risk_score"], 70)
        self.assertEqual(res["risk_level"], "High")

    def test_fake_wfh_telegram_job(self):
        msg = "Congratulations! Part time job work from home earn 2000 daily by liking youtube videos. Join telegram HR."
        res = MessageScanner.analyze(msg)
        self.assertGreaterEqual(res["risk_score"], 50)

    def test_upi_scan_to_receive(self):
        msg = "Sir I transferred money. Please scan this QR code to receive payment into your bank account."
        res = MessageScanner.analyze(msg)
        self.assertGreaterEqual(res["risk_score"], 40)

    def test_legitimate_bank_alert(self):
        msg = "HDFC Bank Alert: An attempt of INR 200 was blocked. If not done by you, block card in NetBanking app. Do not share OTP."
        res = MessageScanner.analyze(msg)
        self.assertLess(res["risk_score"], 50)

    def test_span_offsets(self):
        msg = "Please share your OTP now"
        res = MessageScanner.analyze(msg)
        spans = res.get("highlighted_spans", [])
        self.assertTrue(len(spans) > 0)
        start, end = spans[0]["start"], spans[0]["end"]
        self.assertIn("otp", msg[start:end].lower())

if __name__ == "__main__":
    unittest.main()
