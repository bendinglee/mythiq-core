from flask import Blueprint, request, jsonify
import os, requests

pro_router_bp = Blueprint("pro_router_bp", __name__)
GPT4_KEY = os.getenv("GPT4_API_KEY")

@pro_router_bp.route("/api/proxy/gpt4", methods=["POST"])
def gpt4_proxy():
    data = request.json or {}
    prompt = data.get("query", "").strip()

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GPT4_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
    )
    output = response.json()["choices"][0]["message"]["content"]
    return jsonify({"model": "gpt-4", "response": output})
