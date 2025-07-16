from flask import Blueprint, request, jsonify

emotion_bp = Blueprint("emotion_bp", __name__)

@emotion_bp.route("/anchor", methods=["POST"])
def anchor_emotion():
    anchor = request.json.get("event", "undefined")
    emotion = request.json.get("emotion", "neutral")

    return jsonify({
        "anchor": anchor,
        "emotion_tag": emotion,
        "status": "emotion mapped to anchor"
    })
