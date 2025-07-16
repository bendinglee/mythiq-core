from flask import Blueprint, request, jsonify
import time

experience_bp = Blueprint("experience_bp", __name__)

# 🔄 Save session memory anchors
@experience_bp.route("/save", methods=["POST"])
def save_experience():
    events = request.json.get("events", [])
    session_id = request.json.get("session", f"exp_{int(time.time())}")
    saved = { "session": session_id, "anchors": len(events) }

    return jsonify({
        "experience": saved,
        "status": "experience saved"
    })

# 💭 Generate synthetic dream simulation
@experience_bp.route("/generate", methods=["POST"])
def generate_dream():
    seeds = request.json.get("seeds", [])
    tone = request.json.get("tone", "reflective")

    story = f"Generated dream with {len(seeds)} anchors and tone '{tone}'"

    return jsonify({
        "dream": story,
        "status": "dream logic simulated"
    })

# 📈 Score past timeline of cognition
@experience_bp.route("/score", methods=["POST"])
def score_experience():
    timeline = request.json.get("timeline", [])
    score = sum([len(e.get("label", "")) for e in timeline])

    return jsonify({
        "timeline_length": len(timeline),
        "echo_score": score,
        "status": "experience scored"
    })
