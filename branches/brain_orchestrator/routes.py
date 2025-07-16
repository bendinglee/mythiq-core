from flask import Blueprint, request, jsonify
from .heartbeat import get_uptime
from branches.ai_router.providers import query_openai  # 🧠 New: AI integration

brain_bp = Blueprint("brain_bp", __name__)

# 🧠 Check brain module status
@brain_bp.route("/status", methods=["GET"])
def brain_status():
    return jsonify({
        "brain": "online",
        "uptime": get_uptime(),
        "reflection": "Reflection core activated",
        "status": "ready for cognition"
    })


# 🧠 Accept prompt input and process with real AI
@brain_bp.route("/", methods=["POST"])
def process_brain():
    prompt = request.json.get("prompt", "").strip()

    if not prompt:
        return jsonify({
            "error": "Missing prompt input",
            "status": "failed"
        }), 400

    try:
        # 🔁 Real-time cognition via OpenAI
        response = query_openai(prompt)

        return jsonify({
            "input": prompt,
            "response": response,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500
