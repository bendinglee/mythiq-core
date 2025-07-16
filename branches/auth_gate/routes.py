from flask import Blueprint, request, jsonify
auth_bp = Blueprint("auth_bp", __name__)

VALID_TOKENS = {"pro-demo-001", "gpt-access-999"}  # Replace with real keys

@auth_bp.route("/api/auth/check", methods=["POST"])
def check_access():
    data = request.json or {}
    token = data.get("api_key")

    if token in VALID_TOKENS:
        return jsonify({"tier": "pro", "access": "granted"})
    return jsonify({"tier": "free", "access": "limited"})
