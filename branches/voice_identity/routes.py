from flask import Blueprint, request, jsonify

voice_bp_identity = Blueprint("voice_bp_identity", __name__)

@voice_bp.route("/persona", methods=["POST"])
def voice_persona():
    tone = request.json.get("tone", "neutral")
    emotion = request.json.get("emotion", "stable")

    return jsonify({
        "assigned_voice": {
            "tone": tone,
            "emotion": emotion,
            "profile": f"{tone}_{emotion}"
        },
        "status": "voice persona assigned"
    })
