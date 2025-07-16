from flask import Blueprint, jsonify
import time
import requests
import os

test_bp = Blueprint("test_bp", __name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODELS = ["llama-3.3-70b-versatile", "mistral-saba-24b"]

@test_bp.route("/api/ai-proxy/test", methods=["GET"])
def test_proxy():
    ping_prompt = "Say 'Ping' and identify your model."
    for model in GROQ_MODELS:
        try:
            start = time.time()
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": ping_prompt}],
                    "temperature": 0.0,
                    "max_tokens": 20,
                    "top_p": 1,
                    "stream": False,
                    "stop": None
                },
                timeout=15
            )
            latency = int((time.time() - start) * 1000)
            content = response.json()["choices"][0]["message"]["content"]
            return jsonify({
                "model": model,
                "latency_ms": latency,
                "response": content,
                "status": "online"
            })
        except Exception as e:
            continue
    return jsonify({"status": "offline", "reason": "No working models"}), 503
