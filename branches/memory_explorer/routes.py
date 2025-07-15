from flask import Blueprint, jsonify
import random

explorer_bp = Blueprint("explorer_bp", __name__)

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
