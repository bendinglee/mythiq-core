from flask import Blueprint, request, jsonify
from .persona_mutator import adapt_persona

persona_adapt_bp = Blueprint("persona_adapt_bp", __name__)

@persona_adapt_bp.route("/adapt", methods=["POST"])
def adapt():
    user_signal = request.json.get("input", "")
    return jsonify(adapt_persona(user_signal))
