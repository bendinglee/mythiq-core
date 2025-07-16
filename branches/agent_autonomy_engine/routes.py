from flask import Blueprint, request, jsonify

autonomy_bp = Blueprint("autonomy_bp", __name__)

# 🦾 /agent/autonomy — Toggle autonomous mode
@autonomy_bp.route("/autonomy", methods=["POST"])
def agent_autonomy():
    enabled = request.json.get("enabled", False)
    policy = request.json.get("policy", "reflection-first")

    return jsonify({
        "autonomy_mode": enabled,
        "policy": policy,
        "status": "agent autonomy updated"
    })
