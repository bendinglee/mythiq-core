from flask import Blueprint, request, jsonify
import requests
import os
import time

ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Latest supported Groq models
GROQ_MODELS = [
    "llama-3.3-70b-versatile",  # Highly capable general-purpose model
    "mistral-saba-24b"          # Lightweight high-speed model
]

@ai_proxy_bp.route("/api/ai-proxy", methods=["POST"])
def ai_proxy():
    data = request.json or {}
    prompt = data.get("query", "").strip()
    provider = data.get("provider", "groq")

    if not prompt:
        return jsonify({
            "error": "Missing query content.",
            "status": "failed"
        }), 400

    if provider == "groq":
        for model in GROQ_MODELS:
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
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
                        "stop": None
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    groq_data = response.json()
                    output = groq_data["choices"][0]["message"]["content"]
                    return jsonify({
                        "content": output.strip(),
                        "provider": "groq",
                        "model": model,
                        "timestamp": int(time.time() * 1000)
                    })

                # 🔍 Log deprecation or failure reason (optional for Railway logs)
                print(f"[Groq] Model {model} failed with status: {response.status_code}")

            except Exception as e:
                print(f"[Groq] Model {model} raised exception: {e}")
                continue  # Try next model

        return jsonify({
            "content": "[Fallback] Mythiq could not retrieve a valid response from Groq.",
            "provider": "groq",
            "model": "unavailable",
            "timestamp": int(time.time() * 1000)
        }), 200

    return jsonify({
        "error": "Invalid provider specified.",
        "status": "failed"
    }), 400
