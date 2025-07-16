from flask import Blueprint, request, jsonify
import requests
import os
import time  # ✅ Required for timestamp

ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)

# 🔐 Load API keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@ai_proxy_bp.route("/api/ai-proxy", methods=["POST"])
def ai_proxy():
    data = request.json or {}
    prompt = data.get("query", "").strip()
    provider = data.get("provider", "groq")

    # 🚨 Bonus: Guard against empty input
    if not prompt:
        return jsonify({
            "error": "Missing query content.",
            "status": "failed"
        }), 400

    # 🔁 Groq dispatch logic
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
                        {
                            "role": "system",
                            "content": "You are Mythiq, a fast-thinking AI assistant who responds clearly and efficiently."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "model": "mixtral-8x7b-32768",
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )

            # 🔍 Validate response structure
            if response.status_code != 200:
                return jsonify({
                    "content": f"[Groq] Error: {response.status_code}",
                    "provider": "groq",
                    "model": "mixtral-8x7b",
                    "timestamp": int(time.time() * 1000)
                }), 200  # Soft fail

            data = response.json()
            output = data["choices"][0]["message"]["content"]

            return jsonify({
                "content": output.strip(),
                "provider": "groq",
                "model": "mixtral-8x7b",
                "timestamp": int(time.time() * 1000)
            })

        except Exception as e:
            # ✅ Bonus: Soft fallback for frontend stability
            return jsonify({
                "content": f"[Fallback] Mythiq encountered an error: {str(e)}",
                "provider": "groq",
                "model": "mixtral-8x7b",
                "timestamp": int(time.time() * 1000)
            }), 200

    # 🚨 Unrecognized provider
    return jsonify({
        "error": "Invalid provider specified.",
        "status": "failed"
    }), 400
