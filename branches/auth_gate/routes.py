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

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login endpoint for the authentication module"""
    # This is a mock implementation - in a real system, you would validate credentials
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "token": "sample-auth-token-12345",
        "user": {
            "id": "user-123",
            "name": "Sample User",
            "role": "admin"
        }
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout endpoint for the authentication module"""
    return jsonify({
        "status": "success",
        "message": "Logout successful"
    })

@auth_bp.route("/verify", methods=["POST"])
def verify():
    """Verify a token for the authentication module"""
    # This is a mock implementation - in a real system, you would verify the token
    token = request.json.get("token", "")
    
    if token == "sample-auth-token-12345":
        return jsonify({
            "status": "success",
            "valid": True,
            "user": {
                "id": "user-123",
                "name": "Sample User",
                "role": "admin"
            }
        })
    else:
        return jsonify({
            "status": "error",
            "valid": False,
            "message": "Invalid token"
        }), 401
