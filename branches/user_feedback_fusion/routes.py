from flask import Blueprint, request, jsonify
import time

feedback_bp = Blueprint("feedback_bp", __name__)

# 🔁 Fuse feedback into agent recall
@feedback_bp.route("/fuse", methods=["POST"])
def fuse_feedback():
    feedback = request.json.get("feedback", [])
    score = sum([f.get("rating", 0) for f in feedback])
    fused_note = f"{len(feedback)} feedback points merged"

    return jsonify({
        "fused_score": score,
        "summary": fused_note,
        "status": "feedback fusion complete"
    })

# 💡 Bond score tracking
@feedback_bp.route("/bondscore", methods=["POST"])
def bond_score():
    user = request.json.get("user", "guest")
    agent = request.json.get("agent", "Mythiq")
    score = float(request.json.get("score", 0.5))

    return jsonify({
        "relationship": {
            "user": user,
            "agent": agent,
            "bond_score": score,
            "timestamp": int(time.time())
        },
        "status": "bond score updated"
    })
