from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

# IMPORTANT: This variable name must match exactly what main.py expects
quota_bp = Blueprint("quota_bp", __name__)

@quota_bp.route("/test", methods=["GET"])
def test_quota():
    """Test endpoint for the quota management module"""
    return jsonify({
        "status": "ok",
        "module": "quota",
        "message": "Quota module is alive!"
    })

@quota_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint for the quota management module"""
    # Calculate a future date for reset time (1 month from now)
    reset_time = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return jsonify({
        "status": "operational",
        "module": "quota",
        "current_usage": 125,
        "quota_limit": 1000,
        "remaining": 875,
        "reset_time": reset_time,
        "features": ["basic", "advanced", "enterprise"],
        "version": "1.0.0"
    })
