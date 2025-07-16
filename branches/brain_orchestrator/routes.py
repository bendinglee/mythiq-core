from flask import Blueprint, request, jsonify
from .heartbeat import get_uptime
from branches.ai_router.providers import query_openai

brain_bp = Blueprint("brain_bp", __name__)

@brain_bp.route("/status", methods=["GET"])
def brain_status():
    return jsonify({
        "brain": "online",
        "uptime": get_uptime(),
        "reflection": "Reflection core activated",
        "status": "ready for cognition"
    })

@brain_bp.route("/", methods=["POST"])
def process_brain():
    prompt = request.json.get("prompt", "").strip()
    if not prompt:
        return jsonify({ "error": "Missing prompt input", "status": "failed" }), 400
    response = query_openai(prompt)
    return jsonify({ "input": prompt, "response": response, "status": "success" })
