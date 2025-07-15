from flask import Blueprint, jsonify, request
import random, json, os, time

explorer_bp = Blueprint("explorer_bp", __name__)
SAVE_FILE = "session_memory.json"

# 🔎 Current anchor summary
@explorer_bp.route("/summary", methods=["GET"])
def summary():
    anchors = ["goal_engine", "self_learning", "dialogue_memory"]
    session_id = f"session-{random.randint(1000,9999)}"
    return jsonify({
        "session": session_id,
        "active_anchors": anchors,
        "recall_depth": 3,
        "trigger_trace": [
            "reflect_api",
            "intent_router",
            "persona_adapt_bp"
        ]
    }), 200

# 📜 Session-level journal trace
@explorer_bp.route("/journal", methods=["GET"])
def session_journal():
    return jsonify({
        "session_id": "current",
        "anchors": [
            {"label": "goal_set", "timestamp": 1720728300},
            {"label": "introspect_ping", "timestamp": 1720728460}
        ],
        "summary": "Tracked reflection loops and dispatch signals across active branches."
    }), 200

# 💾 Save memory snapshot
@explorer_bp.route("/save", methods=["POST"])
def save_memory():
    state = request.get_json(silent=True) or {
        "session_id": "auto",
        "anchors": ["goal_engine", "dialogue_memory"],
        "timestamp": time.time()
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        return jsonify({ "status": "saved", "file": SAVE_FILE })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

# 🔁 Load memory snapshot
@explorer_bp.route("/load", methods=["GET"])
def load_memory():
    if not os.path.exists(SAVE_FILE):
        return jsonify({ "error": "no saved memory" }), 404
    try:
        with open(SAVE_FILE) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({ "error": str(e) }), 500
