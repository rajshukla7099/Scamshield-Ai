"""
ScamShield AI - Database Module Re-export
Maintains compatibility with legacy imports while routing to database.db
"""

from database.db import (
    get_db_connection,
    init_db,
    mask_sensitive_info,
    compute_content_hash,
    insert_scan,
    get_recent_scans,
    get_scan_by_id,
    delete_scan,
    clear_all_scans,
    get_dashboard_stats,
    insert_report,
    get_reports,
    update_report_status,
    upvote_report,
    get_quizzes
)

__all__ = [
    "get_db_connection",
    "init_db",
    "mask_sensitive_info",
    "compute_content_hash",
    "insert_scan",
    "get_recent_scans",
    "get_scan_by_id",
    "delete_scan",
    "clear_all_scans",
    "get_dashboard_stats",
    "insert_report",
    "get_reports",
    "update_report_status",
    "upvote_report",
    "get_quizzes"
]
