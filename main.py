from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import traceback
import importlib
import torch
import time

app = Flask(__name__, static_url_path="/static")

# 🚀 Free AI Engine
class FreeAIEngine:
    def __init__(self):
        print("🚀 Loading free AI models...")
        self.text_generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium",
            tokenizer="microsoft/DialoGPT-medium",
            device=0 if torch.cuda.is_available() else -1
        )
        self.qa_model = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad"
        )
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
        print("✅ Free AI models loaded successfully.")

    def generate_response(self, prompt):
        try:
            if self.is_question(prompt):
                return self.answer_question(prompt)
            elif self.needs_summarization(prompt):
                return self.summarize_text(prompt)
            else:
                return self.generate_conversation(prompt)
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def generate_conversation(self, prompt):
        try:
            inputs = self.text_generator.tokenizer.encode(
                prompt + self.text_generator.tokenizer.eos_token,
                return_tensors='pt'
            )
            with torch.no_grad():
                outputs = self.text_generator.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    num_beams=5,
                    no_repeat_ngram_size=2,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.text_generator.tokenizer.eos_token_id
                )
            response = self.text_generator.tokenizer.decode(
                outputs[:, inputs.shape[-1]:][0],
                skip_special_tokens=True
            )
            return response.strip() or "🧠 I need more context to help!"
        except:
            return self.fallback_response(prompt)

    def answer_question(self, question):
        try:
            context = self.get_knowledge_context(question)
            result = self.qa_model(question=question, context=context)
            return result['answer']
        except:
            return self.fallback_response(question)

    def summarize_text(self, text):
        try:
            if len(text) > 100:
                summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
                return summary[0]['summary_text']
            else:
                return text
        except:
            return self.fallback_response(text)

    def is_question(self, text):
        return any(text.lower().startswith(w) for w in [
            'what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should'
        ]) or '?' in text

    def needs_summarization(self, text):
        return len(text.split()) > 50 or 'summarize' in text.lower()

    def get_knowledge_context(self, question):
        knowledge_base = {
            'business': "A business plan includes summary, analysis, marketing, and projections.",
            'technology': "Tech involves computing, AI, innovation, and software.",
            'science': "Science is systematic study of the universe.",
            'health': "Health covers wellness, fitness, and care.",
            'education': "Education is learning via structured methods."
        }
        for topic, context in knowledge_base.items():
            if topic in question.lower():
                return context
        return "General knowledge base."

    def fallback_response(self, prompt):
        if 'business plan' in prompt.lower():
            return (
                "📋 Business Plan Outline:\n"
                "1. Summary\n2. Market Research\n3. Products/Services\n"
                "4. Strategy\n5. Team\n6. Financials"
            )
        elif 'code' in prompt.lower():
            return (
                "💻 Code Help: Use Python, JavaScript, React, Flask.\n"
                "Need help with a snippet or idea?"
            )
        else:
            return f"🤔 I see you're asking about: {prompt}\nLet me explain..."

# 🎯 Initialize AI
free_ai = FreeAIEngine()

# 🔌 Blueprint Injection Logic
def inject_blueprint(path, bp_name, url_prefix):
    try:
        mod = importlib.import_module(path)
        blueprint = getattr(mod, bp_name)
        app.register_blueprint(blueprint, url_prefix=url_prefix)
        print(f"✅ Injected {bp_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed to load {path}.{bp_name}\n{traceback.format_exc()}")

# 🔗 Registered Blueprints
BLUEPRINT_ROUTES = [
    ("branches.auth_gate.routes", "auth_bp", "/api/auth"),
    ("branches.pro_router.routes", "pro_router_bp", "/api/proxy"),
    ("branches.quota.routes", "quota_bp", "/api/quota"),
    ("branches.memory.routes", "memory_bp", "/api/memory"),
    ("branches.reasoning.routes", "reasoning_bp", "/api/reasoning"),  # ✅ Fixed prefix
    ("branches.self_validate.routes", "validation_bp", "/api/validate"),
]

# 🔁 Inject Blueprints
for path, bp_name, prefix in BLUEPRINT_ROUTES:
    inject_blueprint(path, bp_name, prefix)

# 🌐 Default Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# 🧠 Local Brain API
@app.route("/api/brain", methods=["POST"])
def process_brain_request():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({
                "error": "Prompt required",
                "status": "error",
                "timestamp": time.time()
            }), 400

        ai_response = free_ai.generate_response(prompt)

        return jsonify({
            "input": prompt,
            "response": ai_response,
            "status": "success",
            "timestamp": time.time(),
            "metadata": {
                "provider": "huggingface",
                "model": "DialoGPT + DistilBERT + BART",
                "cost": 0.0
            }
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": time.time()
        }), 500

# 🩺 Healthcheck
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq AI Gateway is online ✅",
        "timestamp": time.time()

# 📊 Blueprint Diagnostics Endpoint
@app.route("/api/blueprints", methods=["GET"])
def blueprint_diagnostics():
    return jsonify({
        "status": "success",
        "blueprints": [
            {"module": path, "blueprint": bp_name, "prefix": prefix}
            for path, bp_name, prefix in BLUEPRINT_ROUTES
        ],
        "timestamp": time.time()
    }), 200

# 🔁 Boot Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
