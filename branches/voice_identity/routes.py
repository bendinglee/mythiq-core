from flask import Blueprint, request, jsonify

voice_bp_identity = Blueprint("voice_bp_identity", __name__)

@voice_bp_identity.route("/persona", methods=["POST"])
def load_voice_persona():
    voice = request.json.get("voice", "unknown")
    return jsonify({
        "voice_id": voice,
        "status": "voice persona injected"
    })
