from flask import Blueprint, request, jsonify
from .layout_map import mobile_format
from .voice_hint import generate_hint

mobile_bp = Blueprint("mobile_bp", __name__)

@mobile_bp.route("/hint", methods=["POST"])
def hint():
    msg = request.json.get("text", "")
    return jsonify(generate_hint(msg))

@mobile_bp.route("/persona/compact", methods=["POST"])
def compact():
    raw = request.json.get("text", "")
    return jsonify({ "mobile_view": mobile_format(raw) })
