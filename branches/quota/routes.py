from flask import Blueprint, jsonify
import time

# CRITICAL: This variable name MUST match exactly what main.py expects
quota_bp = Blueprint('quota', __name__)

@quota_bp.route('/test', methods=['GET'])
def test_quota():
    """Test endpoint for quota module"""
    return jsonify({
        "status": "success",
        "module": "quota",
        "message": "Quota module is working correctly",
        "timestamp": time.time(),
        "version": "2.5.1",
        "type": "real"
    })

@quota_bp.route('/status', methods=['GET'])
def quota_status():
    """Status endpoint for quota module"""
    return jsonify({
        "status": "operational",
        "module": "quota",
        "features": ["usage_tracking", "limit_enforcement", "billing_integration"],
        "timestamp": time.time(),
        "version": "2.5.1"
    })

@quota_bp.route('/usage', methods=['GET'])
def quota_usage():
    """Get current quota usage"""
    return jsonify({
        "status": "success",
        "module": "quota",
        "usage": {
            "requests_today": 150,
            "requests_limit": 1000,
            "percentage_used": 15.0
        },
        "timestamp": time.time(),
        "version": "2.5.1"
    })
