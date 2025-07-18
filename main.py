from flask import Flask, request, jsonify, render_template
import torch
import traceback
import time
from transformers import pipeline

app = Flask(__name__, static_url_path="/static")

# ✅ Free AI Engine
class FreeAIEngine:
    def __init__(self):
        print("🚀 Loading free AI models...")
        self.text_generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium",
            tokenizer="microsoft/DialoGPT-medium",
            device=0 if torch.cuda.is_available() else -1
        )
        self.qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
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
            return f"I encountered an error: {str(e)}"

    def generate_conversation(self, prompt):
        try:
            inputs = self.text_generator.tokenizer.encode(
                prompt + self.text_generator.tokenizer.eos_token, return_tensors='pt')
            outputs = self.text_generator.model.generate(
                inputs, max_length=inputs.shape[1] + 100, num_beams=5,
                no_repeat_ngram_size=2, temperature=0.7, do_sample=True,
                pad_token_id=self.text_generator.tokenizer.eos_token_id)
            return self.text_generator.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True).strip()
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
            return text
        except:
            return self.fallback_response(text)

    def is_question(self, text):
        return any(text.lower().startswith(q) for q in ['what', 'how', 'why', 'when', 'where', 'who']) or '?' in text

    def needs_summarization(self, text):
        return len(text.split()) > 50 or 'summarize' in text.lower()

    def get_knowledge_context(self, question):
        base = {
            'business': "Business plan includes summary, market research, structure, finances.",
            'technology': "Technology includes software, AI, hardware, and innovation.",
            'science': "Science is the study of the physical and natural world.",
            'health': "Health includes physical, mental well-being, and care systems.",
            'education': "Education is learning through institutions and experience."
        }
        for k, v in base.items():
            if k in question.lower(): return v
        return "General purpose knowledge base."

    def fallback_response(self, prompt):
        return f"I see you're asking about: {prompt}. Let's explore that."

free_ai = FreeAIEngine()

# 🔌 Blueprint Injection
def inject_blueprint(path, bp_name, url_prefix):
    try:
        mod = __import__(path, fromlist=[bp_name])
        app.register_blueprint(getattr(mod, bp_name), url_prefix=url_prefix)
        print(f"✅ Injected {bp_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed: {path}.{bp_name}\n{traceback.format_exc()}")

# 🔗 Blueprints to Load
BLUEPRINT_ROUTES = [
    ("branches.auth_gate.routes", "auth_bp", "/api/auth"),
    ("branches.pro_router.routes", "pro_router_bp", "/api/proxy"),
    ("branches.quota.routes", "quota_bp", "/api/quota"),
    ("branches.memory.routes", "memory_bp", "/api/memory"),
    ("branches.reasoning.routes", "reasoning_bp", "/api/reasoning"),
    ("branches.self_validate.routes", "validation_bp", "/api/validate"),
    ("branches.ai_proxy.routes", "ai_proxy_bp", "/api/ai-proxy")
]

# 🔁 Register All
for path, bp_name, prefix in BLUEPRINT_ROUTES:
    inject_blueprint(path, bp_name, prefix)

# 🧠 Default Brain Endpoint
@app.route("/api/brain", methods=["POST"])
def process_brain_request():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'No prompt provided', 'status': 'error', 'timestamp': time.time()}), 400
        ai_response = free_ai.generate_response(prompt)
        return jsonify({
            'input': prompt,
            'response': ai_response,
            'status': 'success',
            'timestamp': time.time(),
            'metadata': {
                'provider': 'huggingface_free',
                'model': 'multiple_free_models',
                'cost': 0.00,
                'processing_type': 'local_inference'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'timestamp': time.time()}), 500

# 🌐 Root Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# 📊 Blueprint Diagnostic
@app.route("/api/blueprints", methods=["GET"])
def blueprint_diagnostics():
    return jsonify({
        "status": "success",
        "blueprints": [
            {"module": path, "blueprint": bp_name, "prefix": prefix}
            for path, bp_name, prefix in BLUEPRINT_ROUTES
        ],
        "timestamp": time.time()
    })

# 🧪 Healthcheck
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq Gateway Online",
        "timestamp": time.time()
    }), 200

# 🚀 Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
