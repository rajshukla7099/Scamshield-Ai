"""
ScamShield AI - SQLite Persistence Layer
Next-Generation Cyber Threat Defense & Intelligence Platform

Features:
- Parameterized SQLite queries preventing SQL injection
- Privacy-conscious masking of mobile numbers, emails, and account digits
- SHA-256 deduplication for community scam reports
- Audit trail for scans and risk scores
"""

import sqlite3
import json
import hashlib
import re
from datetime import datetime
from config import Config

def get_db_connection():
    """Returns an SQLite connection with dictionary-like row access."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes the SQLite database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Scans table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_type TEXT NOT NULL,
        target_preview TEXT NOT NULL,
        risk_score INTEGER NOT NULL,
        risk_level TEXT NOT NULL,
        primary_category TEXT NOT NULL,
        indicators_json TEXT,
        recommendations_json TEXT,
        full_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Community reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_type TEXT NOT NULL,
        target_content TEXT NOT NULL,
        content_hash TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        description TEXT,
        risk_assessment TEXT,
        status TEXT DEFAULT 'Pending',
        upvotes INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Educational Quizzes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        scenario_text TEXT NOT NULL,
        source_type TEXT NOT NULL,
        is_scam INTEGER NOT NULL,
        difficulty TEXT NOT NULL,
        category TEXT NOT NULL,
        explanation TEXT NOT NULL,
        red_flags_json TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def mask_sensitive_info(text: str) -> str:
    """Masks phone numbers, emails, and account numbers to protect user privacy."""
    if not text:
        return ""
    # Mask Indian mobile numbers (10 digits, optionally preceded by +91 or 0)
    text = re.sub(r'(\+?91[\-\s]?)?(\d{2})\d{4,6}(\d{2,3})', r'\1\2******\3', text)
    # Mask general emails
    text = re.sub(r'([a-zA-Z0-9_.+-])[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r'\1***@\2', text)
    # Mask 12-16 digit bank / card numbers
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{2,4}[-\s]?\d{2,4}\b', r'****-****-****-XXXX', text)
    return text

def compute_content_hash(text: str) -> str:
    """Computes a normalized SHA-256 hash for deduplication."""
    clean = re.sub(r'\s+', ' ', (text or "").strip().lower())
    return hashlib.sha256(clean.encode('utf-8')).hexdigest()

def insert_scan(scan_type: str, target_preview: str, risk_score: int, risk_level: str,
                primary_category: str, indicators: list, recommendations: list, full_summary: str = "") -> int:
    """Inserts a completed scan record into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ensure sensitive info is masked before storage
    safe_preview = mask_sensitive_info(target_preview)[:140]
    
    cursor.execute("""
        INSERT INTO scans (scan_type, target_preview, risk_score, risk_level, primary_category,
                           indicators_json, recommendations_json, full_summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scan_type,
        safe_preview,
        risk_score,
        risk_level,
        primary_category,
        json.dumps(indicators),
        json.dumps(recommendations),
        full_summary
    ))
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id

def get_recent_scans(limit: int = 50, scan_type: str = None, risk_level: str = None, search: str = None) -> list:
    """Retrieves scan history with optional filters."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM scans WHERE 1=1"
    params = []
    
    if scan_type and scan_type.lower() != 'all':
        query += " AND scan_type = ?"
        params.append(scan_type.lower())
        
    if risk_level and risk_level.lower() != 'all':
        query += " AND risk_level = ?"
        params.append(risk_level.capitalize())
        
    if search:
        query += " AND (target_preview LIKE ? OR primary_category LIKE ?)"
        term = f"%{search.strip()}%"
        params.extend([term, term])
        
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "scan_type": r["scan_type"],
            "target_preview": r["target_preview"],
            "risk_score": r["risk_score"],
            "risk_level": r["risk_level"],
            "primary_category": r["primary_category"],
            "indicators": json.loads(r["indicators_json"] or "[]"),
            "recommendations": json.loads(r["recommendations_json"] or "[]"),
            "full_summary": r["full_summary"],
            "created_at": r["created_at"]
        })
    return results

def get_scan_by_id(scan_id: int) -> dict:
    """Retrieves a single scan by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    r = cursor.fetchone()
    conn.close()
    if not r:
        return None
    return {
        "id": r["id"],
        "scan_type": r["scan_type"],
        "target_preview": r["target_preview"],
        "risk_score": r["risk_score"],
        "risk_level": r["risk_level"],
        "primary_category": r["primary_category"],
        "indicators": json.loads(r["indicators_json"] or "[]"),
        "recommendations": json.loads(r["recommendations_json"] or "[]"),
        "full_summary": r["full_summary"],
        "created_at": r["created_at"]
    }

def delete_scan(scan_id: int) -> bool:
    """Deletes a scan entry by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected

def clear_all_scans() -> bool:
    """Clears all scan history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans;")
    conn.commit()
    conn.close()
    return True

def get_dashboard_stats() -> dict:
    """Aggregates real statistics for dashboard presentation."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM scans")
    total_scans = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as threats FROM scans WHERE risk_level IN ('Medium', 'High')")
    threats_flagged = cursor.fetchone()["threats"]

    cursor.execute("""
        SELECT risk_level, COUNT(*) as count 
        FROM scans 
        GROUP BY risk_level
    """)
    risk_rows = cursor.fetchall()
    risk_dist = {"Low": 0, "Medium": 0, "High": 0}
    for row in risk_rows:
        rl = row["risk_level"]
        if rl in risk_dist:
            risk_dist[rl] = row["count"]

    cursor.execute("""
        SELECT scan_type, COUNT(*) as count 
        FROM scans 
        GROUP BY scan_type
    """)
    type_rows = cursor.fetchall()
    type_dist = {"url": 0, "message": 0}
    for row in type_rows:
        st = row["scan_type"]
        type_dist[st] = row["count"]

    cursor.execute("""
        SELECT primary_category, COUNT(*) as count 
        FROM scans 
        GROUP BY primary_category 
        ORDER BY count DESC 
        LIMIT 6
    """)
    cat_rows = cursor.fetchall()
    top_categories = [{"category": r["primary_category"], "count": r["count"]} for r in cat_rows]

    cursor.execute("SELECT COUNT(*) as total FROM reports")
    total_reports = cursor.fetchone()["total"]

    conn.close()

    return {
        "total_scans": total_scans,
        "threats_flagged": threats_flagged,
        "safe_scans": risk_dist.get("Low", 0),
        "total_reports": total_reports,
        "risk_distribution": risk_dist,
        "type_distribution": type_dist,
        "top_categories": top_categories,
        "recent_scans": get_recent_scans(limit=10)
    }

def insert_report(report_type: str, target_content: str, category: str, description: str, risk_assessment: str) -> dict:
    """Inserts a crowdsourced scam report with deduplication."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_target = mask_sensitive_info(target_content.strip())
    content_hash = compute_content_hash(target_content)
    
    cursor.execute("SELECT id, upvotes FROM reports WHERE content_hash = ?", (content_hash,))
    existing = cursor.fetchone()
    
    if existing:
        new_upvotes = existing["upvotes"] + 1
        cursor.execute("UPDATE reports SET upvotes = ? WHERE id = ?", (new_upvotes, existing["id"]))
        conn.commit()
        conn.close()
        return {"id": existing["id"], "action": "upvoted", "status": "duplicate_upvoted", "upvotes": new_upvotes}
    
    cursor.execute("""
        INSERT INTO reports (report_type, target_content, content_hash, category, description, risk_assessment, upvotes)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    """, (report_type, clean_target, content_hash, category, description, risk_assessment))
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": report_id, "action": "created", "status": "created", "upvotes": 1}

def get_reports(limit: int = 30, status: str = None, category: str = None) -> list:
    """Fetches community reported scams."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM reports WHERE 1=1"
    params = []
    if status and status.lower() != 'all':
        query += " AND status = ?"
        params.append(status.capitalize())
    if category and category.lower() != 'all':
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY upvotes DESC, created_at DESC LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_report_status(report_id: int, new_status: str) -> bool:
    """Updates admin status for community reports."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET status = ? WHERE id = ?", (new_status, report_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected

def upvote_report(report_id: int) -> int:
    """Increments confirmation votes for a report."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET upvotes = upvotes + 1 WHERE id = ?", (report_id,))
    conn.commit()
    cursor.execute("SELECT upvotes FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    return row["upvotes"] if row else 0

def get_quizzes() -> list:
    """Fetches educational interactive quiz scenarios."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quizzes ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    res = []
    for r in rows:
        res.append({
            "id": r["id"],
            "title": r["title"],
            "scenario_text": r["scenario_text"],
            "source_type": r["source_type"],
            "is_scam": bool(r["is_scam"]),
            "difficulty": r["difficulty"],
            "category": r["category"],
            "explanation": r["explanation"],
            "red_flags": json.loads(r["red_flags_json"] or "[]")
        })
    return res
