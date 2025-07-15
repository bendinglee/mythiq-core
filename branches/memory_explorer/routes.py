from flask import Blueprint, jsonify
import random

explorer_bp = Blueprint("explorer_bp", __name__)

@explorer_bp.route("/summary", methods=["GET"])
def summary():
    # Placeholder cognitive state
    anchors = ["goal_engine", "self_learning", "dialogue_memory"]
    session_id = hex(random.randint(1000000,9999999))
    return jsonify({
        "session": session_id,
        "anchors_active": anchors,
        "recall_depth": 3,
        "recent_triggers": ["reflect_api", "intent_router"]
    }), 200
