from flask import Blueprint, jsonify
from .heartbeat import get_uptime

brain_bp = Blueprint("brain_bp", __name__)

@brain_bp.route("/api/brain/status", methods=["GET"])
def brain_status():
    return jsonify({
        "brain": "online",
        "uptime": get_uptime(),
        "reflection": "Reflection core not yet wired"
    })
