from flask import Blueprint, request, jsonify

train_bp_rlstudio = Blueprint("train_bp_rlstudio", __name__)

@train_bp.route("/loop", methods=["POST"])
def train_loop():
    goal = request.json.get("goal", "default")
    result = request.json.get("result", "success")

    score = len(goal) if result == "success" else 0

    return jsonify({
        "goal": goal,
        "result": result,
        "score": score,
        "status": "training loop completed"
    })
