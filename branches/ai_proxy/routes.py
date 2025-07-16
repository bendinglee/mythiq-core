from flask import Blueprint, request, jsonify
import requests
import os
import time

# ✅ Blueprint must be defined at top level for main.py to access it
ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)

# 🔐 Load API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@ai_proxy_bp.route("/api/ai-proxy", methods=["POST"])
def ai_proxy():
    data = request.json or {}
    prompt = data.get("query", "").strip()
    provider = data.get("provider", "groq")

    # 🚨 Input validation
    if not prompt:
        return jsonify({
            "error": "Missing query content.",
            "status": "failed"
        }), 400

    if provider == "groq":
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mixtral-8x7b-32768",  # Valid Groq model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Mythiq, a fast-thinking AI assistant. Respond clearly and helpfully."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "top_p": 1,
                    "stream": False,
                    "stop": None  # Must be Python None, not omitted
                },
                timeout=30
            )

            # 🧪 API Soft-Fail Fallback
            if response.status_code != 200:
                return jsonify({
                    "content": f"[Groq] Error: {response.status_code}",
                    "provider": "groq",
                    "model": "mixtral-8x7b",
                    "timestamp": int(time.time() * 1000)
                }), 200

            # ✅ Success
            groq_data = response.json()
            output = groq_data["choices"][0]["message"]["content"]

            return jsonify({
                "content": output.strip(),
                "provider": "groq",
                "model": "mixtral-8x7b",
                "timestamp": int(time.time() * 1000)
            })

        except Exception as e:
            return jsonify({
                "content": f"[Fallback] Mythiq encountered an error: {str(e)}",
                "provider": "groq",
                "model": "mixtral-8x7b",
                "timestamp": int(time.time() * 1000)
            }), 200

    return jsonify({
        "error": "Invalid provider specified.",
        "status": "failed"
    }), 400
