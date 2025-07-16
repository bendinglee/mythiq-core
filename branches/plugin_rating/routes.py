from flask import Blueprint, request, jsonify

rating_bp = Blueprint("rating_bp", __name__)

@rating_bp.route("/score", methods=["POST"])
def rate_plugin():
    plugin = request.json.get("name", "unknown")
    rating = request.json.get("rating", 0)
    comment = request.json.get("comment", "No feedback")

    return jsonify({
        "plugin": plugin,
        "rating": rating,
        "feedback": comment,
        "status": "plugin scored"
    })
