from flask import Blueprint, request, jsonify
from .tts_connector import synthesize
from .stt_listener import transcribe

voice_bp = Blueprint("voice_bp", __name__)

@voice_bp.route("/speak", methods=["POST"])
def speak():
    txt = request.json.get("text", "")
    return jsonify(synthesize(txt))

@voice_bp.route("/listen", methods=["POST"])
def listen():
    audio_url = request.json.get("audio_url", "")
    return jsonify(transcribe(audio_url))
