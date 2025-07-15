from flask import Blueprint, request, jsonify
from .response_builder import generate_response
from .turn_tracker import log_turn

dialogue_bp = Blueprint("dialogue_bp", __name__)

@dialogue_bp.route("/respond", methods=["POST"])
def respond():
    input_text = request.json.get("input", "")
    reply = generate_response(input_text)
    log_turn(input_text, reply)
    return jsonify({ "response": reply })
