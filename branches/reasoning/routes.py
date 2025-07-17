from flask import Blueprint, request, jsonify
from branches.ai_proxy.thought_chain import build_chain_prompt
import os, time, requests

reasoning_bp = Blueprint("reasoning_bp", __name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@reasoning_bp.route("/api/reason", methods=["POST"])
def reason_cot():
    data = request.json or {}
    query = data.get("query", "")
    chain_prompt = build_chain_prompt(query)

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
            "max_tokens": 1200
        },
        timeout=30
    )

    output = response.json()["choices"][0]["message"]["content"]
    return jsonify({
        "response": output.strip(),
        "timestamp": int(time.time() * 1000)
    })
