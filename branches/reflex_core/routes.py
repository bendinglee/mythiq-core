from flask import Blueprint, request, jsonify
from .reflex_dispatcher import reflex_response
import time

reflex_bp = Blueprint("reflex_bp", __name__)

# 🧠 POST /ping — dispatch reflex from incoming trigger
@reflex_bp.route("/ping", methods=["POST"])
def ping():
    signal = request.json.get("trigger", "")
    return jsonify(reflex_response(signal))

# 🤖 POST /auto — trigger autonomous reflex behavior
@reflex_bp.route("/auto", methods=["POST"])
def reflex_auto():
    trigger = request.json.get("trigger", "none")
    return jsonify({
        "trigger": trigger,
        "reflex_action": f"Auto-response to '{trigger}'",
        "status": "executed",
        "timestamp": int(time.time())
    })

# 🔍 GET /status — show reflex engine mode
@reflex_bp.route("/status", methods=["GET"])
def reflex_status():
    return jsonify({
        "reflex_mode": "adaptive-reactive",
        "uptime": int(time.time()),
        "modules": ["reflex_dispatcher", "reflex_auto"]
    })

# 📈 GET /trace — reflex trace simulation
@reflex_bp.route("/trace", methods=["GET"])
def reflex_trace():
    return jsonify({
        "trace": [
            {"trigger": "persona_shift", "reflex": "goal_reset", "timestamp": int(time.time()) - 150},
            {"trigger": "memory_save", "reflex": "introspect_ping", "timestamp": int(time.time()) - 60}
        ],
        "depth": 2,
        "status": "trace loaded"
    })
