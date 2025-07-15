from flask import Blueprint, request, jsonify
from .reflex_dispatcher import reflex_response

reflex_bp = Blueprint("reflex_bp", __name__)

@reflex_bp.route("/ping", methods=["POST"])
def ping():
    signal = request.json.get("trigger", "")
    return jsonify(reflex_response(signal))
