from flask import Blueprint, request, jsonify

validation_bp = Blueprint("validation_bp", __name__)

def score_output(text):
    flags = ["don't know", "unsure", "cannot answer", "error", "confused"]
    score = 1.0
    for tag in flags:
        if tag in text.lower(): score -= 0.25
    return max(score, 0)

@validation_bp.route("/api/validate", methods=["POST"])
def validate_output():
    data = request.json or {}
    output = data.get("output", "")
    score = score_output(output)

    return jsonify({
        "confidence": round(score, 2),
        "status": "validated",
        "fallback_required": score < 0.4
    })
