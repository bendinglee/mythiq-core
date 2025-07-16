from flask import Blueprint, jsonify
import time

introspect_bp = Blueprint("introspect_bp", __name__)

@introspect_bp.route("/debug", methods=["GET"])
def self_debug():
    return jsonify({
        "status": "stable",
        "uptime": int(time.time()),
        "introspection": {
            "reflex_score": 0.91,
            "goal_alignment": "adaptive",
            "modules_active": 46
        }
    })
