from flask import Blueprint, request, jsonify
from branches.ai_router.providers import generate_response, answer_question, summarize_text

intent_bp = Blueprint("intent_bp", __name__)

@intent_bp.route("/route", methods=["POST"])
def route_intent():
    prompt = request.json.get("prompt", "").lower()

    try:
        if "summarize" in prompt:
            return jsonify({ "intent": "summarize", "response": summarize_text(prompt) })
        elif "what is" in prompt or "who is" in prompt or "explain" in prompt:
            return jsonify({ "intent": "qa", "response": answer_question(prompt, prompt) })
        else:
            return jsonify({ "intent": "chat", "response": generate_response(prompt) })
    except Exception as e:
        return jsonify({ "error": str(e), "status": "error" }), 500
