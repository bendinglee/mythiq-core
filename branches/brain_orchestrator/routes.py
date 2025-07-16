from flask import Blueprint, request, jsonify
from .heartbeat import get_uptime
from branches.reasoning_engine.routes import reason  # 🧠 Phase 3: reasoning handler

brain_bp = Blueprint("brain_bp", __name__)

# 🧠 Module status with uptime and readiness
@brain_bp.route("/status", methods=["GET"])
def brain_status():
    return jsonify({
        "brain": "online",
        "uptime": get_uptime(),
        "reflection": "Reasoning core activated",
        "status": "ready for cognition"
    })


# 🔍 Accept public prompt and route through mesh
@brain_bp.route("/", methods=["POST"])
def process_brain():
    try:
        payload = request.json or {}
        prompt = payload.get("prompt", "").strip()

        if not prompt:
            return jsonify({ "error": "Missing prompt input", "status": "failed" }), 400

        # 🧠 Call full reasoning system
        return reason()

    except Exception as e:
        return jsonify({ "error": str(e), "status": "internal_error" }), 500
