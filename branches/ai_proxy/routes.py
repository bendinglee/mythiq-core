from flask import Blueprint, request, jsonify
import requests
import os

ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@ai_proxy_bp.route("/api/ai-proxy", methods=["POST"])
def ai_proxy():
    data = request.json
    prompt = data.get("query", "")
    provider = data.get("provider", "groq")

    if provider == "groq":
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "messages": [
                        {"role": "system", "content": "You are Mythiq, a fast-thinking AI assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "model": "mixtral-8x7b-32768",
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            )
            data = response.json()
            return jsonify({
                "content": data["choices"][0]["message"]["content"],
                "provider": "groq",
                "model": "mixtral-8x7b",
                "timestamp": int(time.time() * 1000)
            })
        except Exception as e:
            return jsonify({ "error": f"Proxy failed: {str(e)}" }), 500
    else:
        return jsonify({ "error": "Invalid provider" }), 400
