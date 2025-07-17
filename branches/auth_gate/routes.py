from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth_bp", __name__)

# ✅ Replace with real token store or environment lookup
VALID_TOKENS = {"pro-demo-001", "gpt-access-999", "claude-pass-777"}

@auth_bp.route("/api/auth/check", methods=["POST"])
def check_token():
    data = request.json or {}
    token = data.get("api_key", "")

    if token in VALID_TOKENS:
        return jsonify({"tier": "pro", "access": "granted"})
    return jsonify({"tier": "free", "access": "limited"})
