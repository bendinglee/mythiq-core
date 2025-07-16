from flask import Blueprint, request, jsonify

adapt_bp = Blueprint("adapt_bp", __name__)

@adapt_bp.route("/adapt", methods=["POST"])
def adapt_goal():
    feedback = request.json.get("feedback", "neutral")
    adjustment = "goal elevated" if "positive" in feedback else "goal realigned"

    return jsonify({
        "feedback": feedback,
        "adjustment": adjustment,
        "status": "goal adaptation complete"
    })
