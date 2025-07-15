from flask import Blueprint, request, jsonify
from .persona_manager import set_persona, get_persona

persona_bp = Blueprint("persona_bp", __name__)

@persona_bp.route("/set", methods=["POST"])
def set_persona_route():
    config = request.json
    set_persona(config)
    return jsonify({ "status": "success", "config": config })

@persona_bp.route("/get", methods=["GET"])
def get_persona_route():
    return jsonify(get_persona())
