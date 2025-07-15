from flask import Blueprint, jsonify

feedback_api = Blueprint("feedback_api", __name__)

@feedback_api.route("/feedback", methods=["GET"])
def feedback_map():
    return jsonify({
        "modules": ["task_executor", "reflex_core", "goal_engine"],
        "patterns": [
            {"trigger": "self_learning", "response": "reflex_adapt"},
            {"trigger": "persona_shift", "response": "goal_reset"}
        ],
        "status": "feedback mapping online"
    })
