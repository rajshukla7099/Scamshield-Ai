import csv
import io
import json
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, abort
from config import Config
from database.db import (
    init_db, insert_scan, get_recent_scans, get_scan_by_id, delete_scan, clear_all_scans,
    get_dashboard_stats, insert_report, get_reports, update_report_status, upvote_report,
    get_quizzes, mask_sensitive_info
)
from detection.scanner import URLScanner, MessageScanner, AIExplainer, detect_scam, SAMPLE_TEST_CASES
from seed_data import seed_database

app = Flask(__name__)
app.config.from_object(Config)

# Simple in-memory rate limiter per IP for demonstration protection
REQUEST_LOG = {}
RATE_LIMIT_PER_MINUTE = 60

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    clean_history = [t for t in REQUEST_LOG.get(ip, []) if now - t < 60]
    if len(clean_history) >= RATE_LIMIT_PER_MINUTE:
        return True
    clean_history.append(now)
    REQUEST_LOG[ip] = clean_history
    return False

@app.before_request
def check_rate_limit():
    # Exclude static assets
    if request.path.startswith("/static"):
        return None
    client_ip = request.remote_addr or "127.0.0.1"
    if is_rate_limited(client_ip):
        return jsonify({"error": "Rate limit exceeded. Please wait a moment before sending more requests."}), 429

# Auto-seed database on startup if empty
with app.app_context():
    init_db()
    seed_database()

# =====================================================================
# FRONTEND TEMPLATE ROUTES
# =====================================================================

@app.route("/")
def index():
    """Landing Page with Hero, Feature Matrix, and Live Teaser."""
    stats = get_dashboard_stats()
    return render_template("index.html", stats=stats)

@app.route("/dashboard")
def dashboard():
    """Cybersecurity Dashboard with Charts and Metrics."""
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)

@app.route("/scanner")
def scanner():
    """URL Scanner Page."""
    return render_template("scanner.html")

@app.route("/analyzer")
def analyzer():
    """Scam Message Analyzer Page."""
    return render_template("analyzer.html")

@app.route("/results/<int:scan_id>")
def results(scan_id):
    """Detailed Result Page for a specific scan."""
    scan = get_scan_by_id(scan_id)
    if not scan:
        return render_template("404.html", message="Scan report not found."), 404
    return render_template("result.html", scan=scan)

@app.route("/history")
def history():
    """Scan History and Audit Log."""
    return render_template("history.html")

@app.route("/reports")
def reports():
    """Community Scam Radar & Crowd-sourced Reporter."""
    return render_template("reports.html")

@app.route("/learn")
def learn():
    """Cybersecurity Learning Center & Interactive Quizzes."""
    quizzes = get_quizzes()
    return render_template("learn.html", quizzes=quizzes)

@app.route("/about")
def about():
    """About ScamShield AI, Architecture & Legal Disclosures."""
    return render_template("about.html")


# =====================================================================
# JSON REST API ENDPOINTS
# =====================================================================

@app.route("/api/scan", methods=["POST"])
def api_scan():
    """
    Unified scam detection endpoint accepting URLs, SMS, or WhatsApp messages.
    Supports 'auto', 'url', or 'message' type specification.
    """
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or data.get("url") or data.get("message") or "").strip()
    scan_type = data.get("type") or data.get("scan_type") or "auto"

    if not content:
        return jsonify({"success": False, "error": "Input content (URL or message) is required for analysis."}), 400

    if len(content) > 10000:
        return jsonify({"success": False, "error": "Input exceeds maximum allowed length of 10,000 characters."}), 400

    analysis = detect_scam(content, scan_type)
    actual_type = analysis.get("scan_type", "message")
    ai_summary = analysis.get("summary") or AIExplainer.generate_ai_explanation(actual_type, content, analysis)

    # Save to SQLite database
    scan_id = insert_scan(
        scan_type=actual_type,
        target_preview=content[:120],
        risk_score=analysis["risk_score"],
        risk_level=analysis["risk_level"],
        primary_category=analysis["primary_category"],
        indicators=analysis.get("indicators", []),
        recommendations=analysis.get("recommendations", []),
        full_summary=ai_summary
    )

    return jsonify({
        "success": True,
        "scan_id": scan_id,
        "scan_type": actual_type,
        "risk_score": analysis["risk_score"],
        "risk_level": analysis["risk_level"],
        "primary_category": analysis["primary_category"],
        "detected_indicators": analysis.get("detected_indicators", [ind["title"] for ind in analysis.get("indicators", [])]),
        "indicators": analysis.get("indicators", []),
        "explanations": analysis.get("explanations", []),
        "recommendations": analysis.get("recommendations", []),
        "highlighted_spans": analysis.get("highlighted_spans", []),
        "summary": ai_summary,
        "disclaimer": analysis.get("disclaimer", "Automated heuristic estimation. Exercise vigilance when entering credentials."),
        "result": analysis,
        "view_url": f"/results/{scan_id}"
    })

@app.route("/api/samples", methods=["GET"])
def api_samples():
    """Returns curated demo samples for instant threat testing."""
    return jsonify({"success": True, "samples": SAMPLE_TEST_CASES})

@app.route("/api/scan/url", methods=["POST"])
def api_scan_url():
    """Scans a submitted URL using rule heuristics and records the scan."""
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"success": False, "error": "URL parameter is required."}), 400

    if len(url) > 2048:
        return jsonify({"success": False, "error": "URL exceeds maximum allowed length of 2048 characters."}), 400

    # Perform safe heuristic detection (No SSRF, no remote fetching)
    analysis = URLScanner.analyze(url)
    
    # Generate optional explanation synthesis
    ai_summary = AIExplainer.generate_ai_explanation("URL", url, analysis)

    # Save to SQLite database
    scan_id = insert_scan(
        scan_type="url",
        target_preview=url,
        risk_score=analysis["risk_score"],
        risk_level=analysis["risk_level"],
        primary_category=analysis["primary_category"],
        indicators=analysis["indicators"],
        recommendations=analysis["recommendations"],
        full_summary=ai_summary
    )

    return jsonify({
        "success": True,
        "scan_id": scan_id,
        "result": analysis,
        "summary": ai_summary,
        "view_url": f"/results/{scan_id}"
    })

@app.route("/api/scan/message", methods=["POST"])
def api_scan_message():
    """Scans a submitted message for social engineering patterns."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"success": False, "error": "Message text is required."}), 400

    if len(message) > 10000:
        return jsonify({"success": False, "error": "Message exceeds maximum allowed length of 10,000 characters."}), 400

    # Perform multi-lingual and Hinglish analysis
    analysis = MessageScanner.analyze(message)
    
    # Generate synthesis
    ai_summary = AIExplainer.generate_ai_explanation("Message", message, analysis)

    # Save to SQLite database
    scan_id = insert_scan(
        scan_type="message",
        target_preview=message[:100],
        risk_score=analysis["risk_score"],
        risk_level=analysis["risk_level"],
        primary_category=analysis["primary_category"],
        indicators=analysis["indicators"],
        recommendations=analysis["recommendations"],
        full_summary=ai_summary
    )

    return jsonify({
        "success": True,
        "scan_id": scan_id,
        "result": analysis,
        "summary": ai_summary,
        "view_url": f"/results/{scan_id}"
    })

@app.route("/api/stats", methods=["GET"])
def api_stats():
    """Returns real-time aggregated dashboard stats."""
    stats = get_dashboard_stats()
    return jsonify({"success": True, "stats": stats})

@app.route("/api/scans", methods=["GET"])
@app.route("/api/history", methods=["GET"])
def api_get_scans():
    """Fetches scan history with search and filter parameters."""
    scan_type = request.args.get("type")
    risk_level = request.args.get("risk")
    search = request.args.get("search")
    limit = int(request.args.get("limit", 50))

    scans = get_recent_scans(limit=limit, scan_type=scan_type, risk_level=risk_level, search=search)
    return jsonify({"success": True, "scans": scans})

@app.route("/api/scans/<int:scan_id>", methods=["DELETE"])
def api_delete_scan(scan_id):
    """Deletes a specific scan record."""
    success = delete_scan(scan_id)
    if not success:
        return jsonify({"success": False, "error": "Scan record not found or could not be deleted."}), 404
    return jsonify({"success": True, "message": f"Scan #{scan_id} deleted."})

@app.route("/api/scans/clear", methods=["POST", "DELETE"])
@app.route("/api/history/clear", methods=["POST", "DELETE"])
def api_clear_scans():
    """Clears all scan history."""
    clear_all_scans()
    return jsonify({"success": True, "message": "All scan logs successfully cleared."})

@app.route("/api/reports", methods=["GET", "POST"])
def api_reports():
    """Handles community scam reports."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        report_type = data.get("report_type", "url")
        target_content = data.get("target_content", "").strip()
        category = data.get("category", "General Phishing")
        description = data.get("description", "").strip()

        if not target_content:
            return jsonify({"success": False, "error": "Target content (URL, phone, or message) is required."}), 400

        result = insert_report(
            report_type=report_type,
            target_content=target_content,
            category=category,
            description=description,
            risk_assessment="Community Submitted"
        )
        return jsonify({"success": True, "data": result})

    # GET
    status = request.args.get("status")
    category = request.args.get("category")
    reports_list = get_reports(status=status, category=category)
    return jsonify({"success": True, "reports": reports_list})

@app.route("/api/reports/<int:report_id>/upvote", methods=["POST"])
def api_upvote_report(report_id):
    """Increments confirmation votes for a community reported scam."""
    new_votes = upvote_report(report_id)
    return jsonify({"success": True, "upvotes": new_votes})

@app.route("/api/reports/<int:report_id>/status", methods=["POST"])
def api_update_report_status(report_id):
    """Updates admin review status of a report."""
    data = request.get_json(silent=True) or {}
    new_status = data.get("status", "")
    success = update_report_status(report_id, new_status)
    if not success:
        return jsonify({"success": False, "error": "Invalid status or report ID."}), 400
    return jsonify({"success": True, "message": f"Status updated to {new_status}."})

@app.route("/api/quizzes", methods=["GET"])
def api_quizzes():
    """Returns educational scenario quizzes."""
    quizzes = get_quizzes()
    return jsonify({"success": True, "quizzes": quizzes})

@app.route("/api/export/history")
def api_export_history():
    """Exports scan history as CSV or JSON."""
    format_type = request.args.get("format", "csv").lower()
    scans = get_recent_scans(limit=500)

    if format_type == "json":
        return Response(
            json.dumps(scans, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=scamshield_scan_history.json"}
        )

    # CSV output
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Scan Type", "Target Preview", "Risk Score", "Risk Level", "Category", "Date"])

    for s in scans:
        writer.writerow([
            s["id"],
            s["scan_type"],
            s["target_preview"],
            s["risk_score"],
            s["risk_level"],
            s["primary_category"],
            s["created_at"]
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=scamshield_scan_history.csv"}
    )

# =====================================================================
# ERROR HANDLERS
# =====================================================================

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint not found."}), 404
    return render_template("404.html", message="Requested resource could not be found."), 404

@app.errorhandler(500)
def server_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "An internal server error occurred."}), 500
    return render_template("500.html"), 500

if __name__ == "__main__":
    print(f"🛡️ ScamShield AI running on http://127.0.0.1:{Config.PORT}")
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
