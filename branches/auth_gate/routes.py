from flask import Blueprint, jsonify, request

# IMPORTANT: This variable name must match exactly what main.py expects
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/test", methods=["GET"])
def test_auth():
    """Test endpoint for the authentication module"""
    return jsonify({
        "status": "ok",
        "module": "auth_gate",
        "message": "Auth route is working!"
    })

@auth_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint for the authentication module"""
    return jsonify({
        "status": "operational",
        "module": "auth_gate",
        "authenticated": False,
        "user": "anonymous",
        "permissions": ["read"],
        "session_active": True,
        "features": ["basic", "advanced", "enterprise"],
        "version": "1.0.0"
    })
