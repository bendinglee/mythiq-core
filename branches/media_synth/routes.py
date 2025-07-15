from flask import Blueprint, request, jsonify
from .fusion_builder import build_storyboard

media_bp = Blueprint("media_bp", __name__)

@media_bp.route("/synth", methods=["POST"])
def synth():
    inputs = request.json
    return jsonify(build_storyboard(inputs))
