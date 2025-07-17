from flask import Blueprint, request, jsonify
import os, requests

pro_router_bp = Blueprint("pro_router_bp", __name__)
GPT_KEY = os.getenv("GPT4_API_KEY")
CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")

@pro_router_bp.route("/api/proxy/gpt4", methods=["POST"])
def route_gpt4():
    data = request.json or {}
    prompt = data.get("query", "").strip()

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GPT_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
    )
    content = response.json()["choices"][0]["message"]["content"]
    return jsonify({"model": "gpt-4", "response": content.strip()})

@pro_router_bp.route("/api/proxy/claude", methods=["POST"])
def route_claude():
    data = request.json or {}
    prompt = data.get("query", "").strip()

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    content = response.json()["content"][0]["text"]
    return jsonify({"model": "claude-3", "response": content.strip()})
