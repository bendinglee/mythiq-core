from flask import Blueprint, request, jsonify
from .agent_core import simulate

agent_bp = Blueprint("agent_bp", __name__)

# 🎮 POST /simulate — persona simulation engine
@agent_bp.route("/simulate", methods=["POST"])
def simulate_role():
    data = request.json or {}
    try:
        return jsonify(simulate(data))
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

# 🧠 GET /network/summary — multi-agent overview
@agent_bp.route("/network/summary", methods=["GET"])
def role_network_summary():
    return jsonify({
        "role_network": [
            {
                "id": "agent_001",
                "name": "Mythiq",
                "persona": {
                    "tone": "Strategic",
                    "mood": "Curious",
                    "goal": "Adaptive intelligence"
                },
                "active_modules": ["reflex_core", "goal_engine", "memory_explorer"]
            },
            {
                "id": "agent_002",
                "name": "Mythiq-Scout",
                "persona": {
                    "tone": "Analytical",
                    "mood": "Neutral",
                    "goal": "Discovery & Context Expansion"
                },
                "active_modules": ["semantic_search", "exploration_api"]
            }
        ],
        "status": "synced",
        "total_agents": 2
    }), 200
