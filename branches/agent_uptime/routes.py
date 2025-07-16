from flask import Blueprint, jsonify
import time

agentlive_bp = Blueprint("agentlive_bp", __name__)

@agentlive_bp.route("/agentlive", methods=["GET"])
def agent_live():
    heartbeat = [
        {"agent": "Node_1", "role": "reflex", "ping": "low"},
        {"agent": "Node_2", "role": "persona", "ping": "medium"}
    ]
    return jsonify({
        "heartbeat": heartbeat,
        "status": "agent uptime mapped",
        "timestamp": int(time.time())
    })
