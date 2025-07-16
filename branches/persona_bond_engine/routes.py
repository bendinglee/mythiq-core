from flask import Blueprint, request, jsonify

bond_bp = Blueprint("bond_bp", __name__)

# 🧬 Synchronize user and agent persona traits
@bond_bp.route("/sync", methods=["POST"])
def sync_persona():
    user_traits = request.json.get("user", {})
    agent_traits = request.json.get("agent", {})

    merged = {
        "identity": user_traits.get("name", "guest") + "-" + agent_traits.get("name", "Mythiq"),
        "tone": agent_traits.get("tone", "adaptive"),
        "goal": agent_traits.get("goal", "evolve with empathy")
    }

    return jsonify({
        "merged_persona": merged,
        "status": "persona crossover complete"
    })
