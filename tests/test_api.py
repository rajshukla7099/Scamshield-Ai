import unittest
import json
from app import app
from database import init_db

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()
        init_db()

    def test_pages_load(self):
        endpoints = ["/", "/dashboard", "/scanner", "/analyzer", "/history", "/reports", "/learn", "/about"]
        for ep in endpoints:
            response = self.client.get(ep)
            self.assertEqual(response.status_code, 200, f"Endpoint {ep} failed to load.")

    def test_api_scan_url_success(self):
        payload = {"url": "http://sbi-kyc-update.xyz/login"}
        response = self.client.post(
            "/api/scan/url",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("scan_id", data)
        self.assertGreaterEqual(data["result"]["risk_score"], 50)

    def test_api_scan_url_empty_validation(self):
        response = self.client.post(
            "/api/scan/url",
            data=json.dumps({"url": ""}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_api_scan_message_success(self):
        payload = {"message": "Aapka bijli connection aaj raat kat diya jayega electricity bill update kare"}
        response = self.client.post(
            "/api/scan/message",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("scan_id", data)
        self.assertIn("indicators", data["result"])

    def test_api_stats(self):
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("total_scans", data["stats"])
        self.assertIn("risk_distribution", data["stats"])

    def test_api_reports_crud(self):
        # Create report
        payload = {
            "report_type": "phone",
            "target_content": "+91 9999888877",
            "category": "Utility Scam",
            "description": "Caller claimed electricity power cut"
        }
        res1 = self.client.post("/api/reports", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertTrue(data1["success"])
        report_id = data1["data"]["id"]

        # Duplicate check - same payload should increment upvotes instead of duplicating
        res2 = self.client.post("/api/reports", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)
        self.assertEqual(data2["data"]["status"], "duplicate_upvoted")

        # Upvote endpoint
        res3 = self.client.post(f"/api/reports/{report_id}/upvote")
        self.assertEqual(res3.status_code, 200)

        # Status update
        res4 = self.client.post(f"/api/reports/{report_id}/status", data=json.dumps({"status": "Verified Scam"}), content_type="application/json")
        self.assertEqual(res4.status_code, 200)

    def test_export_endpoints(self):
        res_csv = self.client.get("/api/export/history?format=csv")
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn("text/csv", res_csv.headers.get("Content-Type", ""))

        res_json = self.client.get("/api/export/history?format=json")
        self.assertEqual(res_json.status_code, 200)
        self.assertIn("application/json", res_json.headers.get("Content-Type", ""))

    def test_unified_api_scan(self):
        # Auto-detect URL
        res_url = self.client.post(
            "/api/scan",
            data=json.dumps({"content": "http://192.168.1.1/admin/login", "type": "auto"}),
            content_type="application/json"
        )
        self.assertEqual(res_url.status_code, 200)
        data_url = json.loads(res_url.data)
        self.assertTrue(data_url["success"])
        self.assertEqual(data_url["scan_type"], "url")
        self.assertIn("risk_score", data_url)

        # Auto-detect Message
        res_msg = self.client.post(
            "/api/scan",
            data=json.dumps({"content": "Please share your OTP and enter UPI PIN", "type": "auto"}),
            content_type="application/json"
        )
        self.assertEqual(res_msg.status_code, 200)
        data_msg = json.loads(res_msg.data)
        self.assertTrue(data_msg["success"])
        self.assertEqual(data_msg["scan_type"], "message")
        self.assertIn("risk_score", data_msg)

    def test_samples_and_history_endpoints(self):
        # Test /api/samples
        res_samples = self.client.get("/api/samples")
        self.assertEqual(res_samples.status_code, 200)
        samples = json.loads(res_samples.data)
        self.assertTrue(samples["success"])
        self.assertIn("samples", samples)

        # Test /api/history alias
        res_hist = self.client.get("/api/history")
        self.assertEqual(res_hist.status_code, 200)
        hist = json.loads(res_hist.data)
        self.assertTrue(hist["success"])
        self.assertIn("scans", hist)

        # Test /api/history/clear alias
        res_clear = self.client.post("/api/history/clear")
        self.assertEqual(res_clear.status_code, 200)
        clear_data = json.loads(res_clear.data)
        self.assertTrue(clear_data["success"])

if __name__ == "__main__":
    unittest.main()
