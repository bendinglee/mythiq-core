from flask import Blueprint, request, jsonify

mission_bp = Blueprint("mission_bp", __name__)

# 🛠 /mission/build — Design mission plan
@mission_bp.route("/build", methods=["POST"])
def build_mission():
    goal = request.json.get("goal", "self-evolution")
    steps = request.json.get("steps", [])
    plan = f"{len(steps)} steps to accomplish '{goal}'"

    return jsonify({
        "goal": goal,
        "steps": steps,
        "summary": plan,
        "status": "mission crafted"
    })

# 📊 /mission/eval — Evaluate mission efficiency
@mission_bp.route("/eval", methods=["POST"])
def evaluate_mission():
    mission = request.json.get("goal", "undefined")
    feedback = request.json.get("feedback", [])
    score = sum([f.get("impact", 0) for f in feedback])

    return jsonify({
        "mission": mission,
        "feedback": feedback,
        "impact_score": score,
        "status": "mission evaluated"
    })
