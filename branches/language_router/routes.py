from flask import Blueprint, request, jsonify
from .language_classifier import detect_lang
from .intent_adapter import route_intent

lang_bp = Blueprint("lang_bp", __name__)

@lang_bp.route("/route", methods=["POST"])
def route():
    text = request.json.get("text", "")
    lang = detect_lang(text)
    path = route_intent(lang, text)
    return jsonify({ "language": lang, "path": path })

@lang_bp.route("/translate", methods=["POST"])
def translate():
    return jsonify({ "output": "Feature ready soon" })
