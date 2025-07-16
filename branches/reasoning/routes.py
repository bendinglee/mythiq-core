from flask import Blueprint, request, jsonify
from branches.ai_proxy.thought_chain import build_chain_prompt
import requests, os

reasoning_bp = Blueprint("reasoning_bp", __name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@reasoning_bp.route("/api/reason", methods=["POST"])
def reason_through():
    data = request.json or {}
    user_query = data.get("query", "").strip()
    chain_prompt = build_chain_prompt(user_query)

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": chain_prompt}],
            "temperature": 0.3,
            "max_tokens": 1200,
            "top_p": 1,
            "stream": False,
            "stop": None
        },
        timeout=30
    )
    output = response.json()["choices"][0]["message"]["content"]
    return jsonify({
        "response": output.strip(),
        "timestamp": int(time.time() * 1000)
    })
