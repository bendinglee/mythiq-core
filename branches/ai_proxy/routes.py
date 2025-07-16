from flask import Blueprint, request, jsonify
import requests
import os
import time
from .thought_chain import build_chain_prompt

ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)

# 🔐 Load keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GPT4_API_KEY = os.getenv("GPT4_API_KEY")

# 🔄 Groq models in fallback order
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "mistral-saba-24b"
]

# 🎭 Persona system prompts
PERSONA_MAP = {
    "analyst": "You are Mythiq, a highly analytical assistant focused on precise, evidence-based reasoning.",
    "mentor": "You are Mythiq, a warm, encouraging mentor who guides with empathy and clarity.",
    "explorer": "You are Mythiq, an imaginative explorer who shares ideas with curiosity and creativity.",
    "default": "You are Mythiq, a fast-thinking AI assistant who responds clearly and helpfully."
}

# 🔑 Demo: list of Pro tokens
VALID_TOKENS = {"pro-demo-001", "gpt-access-999"}

@ai_proxy_bp.route("/api/ai-proxy", methods=["POST"])
def ai_proxy():
    data = request.json or {}
    prompt = data.get("query", "").strip()
    persona = data.get("persona", "default").lower()
    provider = data.get("provider", "groq")
    token = data.get("api_key", "")

    if not prompt:
        return jsonify({
            "error": "Missing query content.",
            "status": "failed"
        }), 400

    system_prompt = PERSONA_MAP.get(persona, PERSONA_MAP["default"])

    # 🧠 Add chain-of-thought reasoning for analyst persona
    if persona == "analyst":
        prompt = build_chain_prompt(prompt)

    # 🔓 PRO TIER: route to GPT-4 if token matches
    if token in VALID_TOKENS and provider == "gpt4":
        try:
            start_time = time.time()
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GPT4_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )
            latency_ms = int((time.time() - start_time) * 1000)
            output = response.json()["choices"][0]["message"]["content"]

            return jsonify({
                "content": output.strip(),
                "provider": "openai",
                "model": "gpt-4",
                "latency_ms": latency_ms,
                "timestamp": int(time.time() * 1000)
            })

        except Exception as e:
            return jsonify({
                "error": f"GPT-4 error: {str(e)}",
                "status": "failed"
            }), 500

    # 🌐 FREE TIER: fallback-safe Groq model rotation
    if provider == "groq":
        for model in GROQ_MODELS:
            try:
                start_time = time.time()
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000,
                        "top_p": 1,
                        "stream": False,
                        "stop": None
                    },
                    timeout=30
                )
                latency_ms = int((time.time() - start_time) * 1000)

                if response.status_code == 200:
                    groq_data = response.json()
                    output = groq_data["choices"][0]["message"]["content"]

                    # 🧪 Basic validation
                    if any(tag in output.lower() for tag in ["i don't know", "can't answer", "unsure"]):
                        output = "[Retry] Mythiq did not confidently answer."

                    return jsonify({
                        "content": output.strip(),
                        "provider": "groq",
                        "model": model,
                        "latency_ms": latency_ms,
                        "timestamp": int(time.time() * 1000)
                    })

            except Exception as e:
                print(f"[Groq Fallback] Model {model} error: {e}")
                continue

        return jsonify({
            "content": "[Fallback] No valid response from Groq.",
            "provider": "groq",
            "model": "unavailable",
            "timestamp": int(time.time() * 1000)
        }), 200

    return jsonify({
        "error": "Invalid provider specified or no valid token.",
        "status": "failed"
    }), 400


# ✅ Telemetry Endpoint
@ai_proxy_bp.route("/api/ai-proxy/test", methods=["GET"])
def proxy_test():
    test_prompt = "Say 'Ping' and identify your model."
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
                    "messages": [{"role": "user", "content": test_prompt}],
                    "temperature": 0,
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
                "status": "healthy"
            })

        except Exception as e:
            print(f"[Test] Model {model} failed: {e}")
            continue

    return jsonify({
        "status": "offline",
        "models_checked": GROQ_MODELS
    }), 503
