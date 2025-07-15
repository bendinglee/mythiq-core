from flask import Blueprint, request, jsonify
from .layout_map import mobile_format
from .voice_hint import generate_hint
import time

mobile_bp = Blueprint("mobile_bp", __name__)

# 🎧 POST /hint — voice tone suggestion
@mobile_bp.route("/hint", methods=["POST"])
def hint():
    msg = request.json.get("text", "")
    return jsonify(generate_hint(msg))

# 📱 POST /persona/compact — compress persona text for mobile
@mobile_bp.route("/persona/compact", methods=["POST"])
def compact():
    raw = request.json.get("text", "")
    return jsonify({ "mobile_view": mobile_format(raw) })

# 📡 GET /ping — confirm mobile mode compatibility
@mobile_bp.route("/ping", methods=["GET"])
def mobile_ping():
    return jsonify({
        "mobile_mode": "active",
        "compatible": True,
        "context_mode": "compressed-reflection",
        "timestamp": int(time.time())
    }), 200

# 🔁 POST /context — device-aware context modulator
@mobile_bp.route("/context", methods=["POST"])
def mobile_context():
    client = request.json or {}
    device = client.get("device", "unknown")
    screen = client.get("screen_size", "default")
    tone = client.get("tone", "neutral")

    return jsonify({
        "device": device,
        "screen": screen,
        "persona_adjustment": {
            "tone": tone,
            "style": "condensed",
            "goal": "Rapid assist"
        },
        "context_mode": "mobile",
        "response": f"Adjusted context for device: {device}"
    }), 200
