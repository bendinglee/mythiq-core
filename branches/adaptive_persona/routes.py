from flask import Blueprint, request, jsonify
from .persona_mutator import adapt_persona

# 🎭 Adaptive persona blueprint
persona_adapt_bp = Blueprint("persona_adapt_bp", __name__)

# 🔁 POST /adapt — generate persona mutation from input signal
@persona_adapt_bp.route("/adapt", methods=["POST"])
def adapt():
    user_signal = request.json.get("input", "")
    return jsonify(adapt_persona(user_signal))

# 🧬 POST /reflect — update persona tone, mood, goals directly
@persona_adapt_bp.route("/reflect", methods=["POST"])
def reflect_persona():
    data = request.json or {}
    tone = data.get("tone", "Curious")
    mood = data.get("mood", "Neutral")
    goal = data.get("goal", "Self-evolution")

    return jsonify({
        "status": "updated",
        "persona": {
            "tone": tone,
            "mood": mood,
            "goal": goal
        }
    }), 200
