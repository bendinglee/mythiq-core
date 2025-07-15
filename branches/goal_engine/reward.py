from flask import Blueprint, request, jsonify

reward_bp = Blueprint("reward_bp", __name__)

@reward_bp.route("/score", methods=["POST"])
def score_goal():
    goal = request.json.get("goal", "")
    result = request.json.get("result", "")
    score = len(result)  # example metric

    return jsonify({
        "goal": goal,
        "result": result,
        "score": score,
        "status": "scored"
    })

@reward_bp.route("/reward", methods=["POST"])
def give_reward():
    agent = request.json.get("agent", "none")
    points = request.json.get("points", 0)

    return jsonify({
        "agent": agent,
        "reward": points,
        "status": "reinforcement delivered"
    })
