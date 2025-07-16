from flask import Blueprint, request, jsonify

validation_bp = Blueprint("validation_bp", __name__)

def score_confidence(output):
    flags = ["don't know", "unable", "cannot", "unsure", "hallucination"]
    score = 1.0
    for flag in flags:
        if flag in output.lower():
            score -= 0.3
    return max(score, 0)

@validation_bp.route("/api/validate", methods=["POST"])
def validate_output():
    data = request.json or {}
    output = data.get("output", "")
    confidence = score_confidence(output)
    return jsonify({
        "confidence_score": round(confidence, 2),
        "status": "validated",
        "fallback_required": confidence < 0.4
    })
