"""
AI Proxy Module - GROQ Model Ping Test
Mythiq Gateway Enterprise v2.5.1
"""

from flask import Blueprint, jsonify
import time
import requests
import os

# Create the test_bp blueprint with exact variable name expected by main.py
test_bp = Blueprint("test_bp", __name__)

# Load GROQ API key and model list
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODELS = ["llama-3.3-70b-versatile", "mistral-saba-24b"]

@test_bp.route("/test", methods=["GET"])
def test_proxy():
    """Ping GROQ models and return latency + response"""
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
                "status": "online",
                "version": "2.5.1",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })

        except Exception as e:
            continue

    return jsonify({
        "status": "offline",
        "reason": "No working models",
        "version": "2.5.1",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }), 503
