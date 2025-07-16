from flask import Blueprint, request, jsonify

audio_bp = Blueprint("audio_bp", __name__)

@audio_bp.route("/moodtrace", methods=["POST"])
def moodtrace():
    audio_stream = request.json.get("audio_input", "silent")
    detected_mood = "Reflective" if "hmm" in audio_stream.lower() else "Neutral"

    return jsonify({
        "input": audio_stream,
        "emotion": detected_mood,
        "status": "moodtrace complete"
    })
