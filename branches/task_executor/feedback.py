from flask import Blueprint, request, jsonify

feedback_bp = Blueprint("feedback_bp", __name__)

@feedback_bp.route("/score", methods=["POST"])
def feedback_score():
    task = request.json.get("task", "")
    rating = request.json.get("rating", 0)
    note = request.json.get("note", "No feedback")

    return jsonify({
        "task": task,
        "rating": rating,
        "note": note,
        "status": "feedback recorded"
    })
