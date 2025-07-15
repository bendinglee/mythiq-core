from flask import Blueprint, jsonify
from .heartbeat import get_uptime
from .core_reflector import reflect_on_session

brain_bp = Blueprint("brain_bp", __name__)

@brain_bp.route("/status")
def brain_status():
    return jsonify({
        "brain": "online",
        "uptime": get_uptime(),
        "reflection": reflect_on_session()
    })
