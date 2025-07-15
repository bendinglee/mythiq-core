from flask import Blueprint, request, jsonify
from .classifier import classify_intent

intent_bp = Blueprint("intent_bp", __name__)

@intent_bp.route("/route", methods=["POST"])
def route_input():
    query = request.json.get("input", "")
    intent = classify_intent(query)
    return jsonify({ "intent": intent })
