from flask import Blueprint, request, jsonify
from .heartbeat import get_uptime

brain_bp = Blueprint("brain_bp", __name__)

# 🧠 Check brain module status
@brain_bp.route("/status", methods=["GET"])
def brain_status():
    return jsonify({
        "brain": "online",
        "uptime": get_uptime(),
        "reflection": "Reflection core activated",
        "status": "ready for cognition"
    })

# 🧠 Accept prompt input from frontend
@brain_bp.route("/", methods=["POST"])
def process_brain():
    try:
        payload = request.json or {}
        user_query = payload.get("prompt", "").strip()

        if not user_query:
            return jsonify({
                "error": "Missing prompt input",
                "status": "failed"
            }), 400

        # 🧠 Replace this with actual brain processing logic later
        processed_output = f"Processed brain signal → '{user_query}'"

        return jsonify({
            "input": user_query,
            "response": processed_output,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "internal_error"
        }), 500
