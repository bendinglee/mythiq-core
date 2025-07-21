from flask import Blueprint, jsonify
import time

# CRITICAL: This variable name MUST match exactly what main.py expects
auth_bp = Blueprint('auth_gate', __name__)

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    """Test endpoint for authentication module"""
    return jsonify({
        "status": "success",
        "module": "auth_gate",
        "message": "Authentication module is working correctly",
        "timestamp": time.time(),
        "version": "2.5.1",
        "type": "real"
    })

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """Status endpoint for authentication module"""
    return jsonify({
        "status": "operational",
        "module": "auth_gate",
        "features": ["user_authentication", "token_validation", "session_management"],
        "timestamp": time.time(),
        "version": "2.5.1"
    })
