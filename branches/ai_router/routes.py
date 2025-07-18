from flask import Blueprint, request, jsonify
from .providers import (
    query_openai,
    query_claude,
    generate_response,
    answer_question,
    summarize_text
)

ai_router_bp = Blueprint("ai_router_bp", __name__)

@ai_router_bp.route("/query", methods=["POST"])
def route_ai():
    prompt = request.json.get("prompt", "").strip()
    if not prompt:
        return jsonify({ "error": "No prompt provided", "status": "failed" }), 400

    try:
        response = query_openai(prompt)
    except Exception as e1:
        try:
            response = query_claude(prompt)
        except Exception as e2:
            return jsonify({
                "error": f"OpenAI failed: {str(e1)} | Claude failed: {str(e2)}",
                "status": "error"
            }), 500

    return jsonify({ "input": prompt, "response": response, "status": "success" })

@ai_router_bp.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt", "")
    if not prompt:
        return jsonify({ "error": "Missing prompt for generation" }), 400
    return jsonify({ "response": generate_response(prompt) })

@ai_router_bp.route("/qa", methods=["POST"])
def qa():
    context = request.json.get("context", "")
    question = request.json.get("question", "")
    if not context or not question:
        return jsonify({ "error": "Missing context or question" }), 400
    return jsonify({ "answer": answer_question(context, question) })

@ai_router_bp.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text", "")
    if not text:
        return jsonify({ "error": "Missing text for summarization" }), 400
    return jsonify({ "summary": summarize_text(text) })
