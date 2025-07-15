from flask import Blueprint, request, jsonify
from .persona_mutator import adapt_persona
import json, os, time

# 🎭 Adaptive persona blueprint
persona_adapt_bp = Blueprint("persona_adapt_bp", __name__)
HISTORY_FILE = "persona_history.json"

# 🔁 POST /adapt — generate persona mutation from input signal
@persona_adapt_bp.route("/adapt", methods=["POST"])
def adapt():
    user_signal = request.json.get("input", "")
    return jsonify(adapt_persona(user_signal))

# 🧬 POST /reflect — update persona tone, mood, goals directly + log history
@persona_adapt_bp.route("/reflect", methods=["POST"])
def reflect_persona():
    data = request.json or {}
    record = {
        "timestamp": time.time(),
        "tone": data.get("tone", "Curious"),
        "mood": data.get("mood", "Neutral"),
        "goal": data.get("goal", "Self-evolution")
    }

    # 🔒 Load & append history safely
    history = []
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        history.append(record)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

    return jsonify({ "status": "updated", "persona": record }), 200

# 📜 GET /reflect/history — return full timeline of persona reflection
@persona_adapt_bp.route("/reflect/history", methods=["GET"])
def get_reflection_history():
    try:
        if not os.path.exists(HISTORY_FILE):
            return jsonify({ "history": [] })
        with open(HISTORY_FILE) as f:
            return jsonify({ "history": json.load(f) })
    except Exception as e:
        return jsonify({ "error": str(e), "history": [] }), 500
