from flask import Blueprint, request, jsonify
from .task_relay import relay_task
from .agent_registry import connect_agent

mesh_bp = Blueprint("mesh_bp", __name__)

# 📡 Broadcast readiness ping + identity
@mesh_bp.route("/ping", methods=["GET"])
def mesh_ping():
    return jsonify({
        "mesh_status": "online",
        "message": "Mythiq mesh broadcasting is active.",
        "agent_signature": {
            "name": "Mythiq",
            "version": "v1-core",
            "goal_mode": "adaptive-reflex",
            "personality": {
                "tone": "Supportive",
                "style": "Curious",
                "evolution": "Reflective"
            }
        }
    }), 200

# 🤝 POST /connect — register external agent
@mesh_bp.route("/connect", methods=["POST"])
def connect():
    data = request.json or {}
    try:
        return jsonify(connect_agent(data))
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

# 🚦 POST /task/relay — relay goal/task to another agent
@mesh_bp.route("/task/relay", methods=["POST"])
def relay():
    data = request.json or {}
    try:
        return jsonify(relay_task(data))
    except Exception as e:
        return jsonify({ "error": str(e) }), 500
