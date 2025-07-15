from flask import Blueprint, request, jsonify
from .context_stitcher import build_context_prompt

context_bp = Blueprint("context_bp", __name__)

@context_bp.route("/get", methods=["POST"])
def get_context():
    data = request.json
    user_input = data.get("input", "")
    stitched = build_context_prompt(user_input)
    return jsonify({ "context_prompt": stitched })
