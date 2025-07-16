from flask import Blueprint, request, jsonify
from branches.ai_router.providers import generate_response, answer_question, summarize_text

intent_bp = Blueprint("intent_bp", __name__)

def detect_intent(prompt):
    prompt = prompt.lower()
    if prompt.startswith("summarize") or "tl;dr" in prompt:
        return "summarization"
    elif any(q in prompt for q in ["who", "what", "when", "where", "how", "why", "explain"]):
        return "qa"
    elif "write" in prompt or "generate" in prompt or "story" in prompt:
        return "generation"
    elif "analyze" in prompt or "reason" in prompt or "steps" in prompt:
        return "reasoning"
    else:
        return "chat"

@intent_bp.route("/api/intent/route", methods=["POST"])
def route_intent():
    data = request.json or {}
    prompt = data.get("query", "").strip()

    if not prompt:
        return jsonify({ "error": "Missing query content." }), 400

    intent = detect_intent(prompt)

    try:
        if intent == "summarization":
            response = summarize_text(prompt)
        elif intent == "qa":
            response = answer_question(prompt, prompt)
        elif intent == "generation":
            response = generate_response(f"Write something creative based on: {prompt}")
        elif intent == "reasoning":
            response = generate_response(f"Let's reason step by step. Question: {prompt}")
        else:
            response = generate_response(prompt)

        return jsonify({
            "intent": intent,
            "response": response
        })

    except Exception as e:
        return jsonify({
            "intent": intent,
            "error": str(e),
            "status": "failed"
        }), 500
