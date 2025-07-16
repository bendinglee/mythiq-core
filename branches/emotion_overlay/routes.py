from flask import Blueprint, request, jsonify

emotion_bp = Blueprint("emotion_bp", __name__)

@emotion_bp.route("/overlay", methods=["POST"])
def overlay():
    input_data = request.json or {}
    tone = input_data.get("tone", "neutral")
    source = input_data.get("source", "gallery")
    mapped = {
        "neutral": "#CCCCCC",
        "curious": "#99CCFF",
        "introspective": "#666699",
        "reflective": "#FFCC66"
    }

    return jsonify({
        "overlay": {
            "source": source,
            "tone": tone,
            "color": mapped.get(tone, "#DDDDDD")
        },
        "status": "emotional overlay applied"
    })
