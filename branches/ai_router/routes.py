from flask import Blueprint, request, jsonify
from .providers import query_openai, query_claude

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
            return jsonify({ "error": f"OpenAI failed: {str(e1)} | Claude failed: {str(e2)}", "status": "error" }), 500

    return jsonify({
        "input": prompt,
        "response": response,
        "status": "success"
    })
