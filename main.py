from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import torch
import traceback
import time

app = Flask(__name__, static_url_path="/static")

# ✅ Free AI Engine Class
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
            return f"I encountered an error: {str(e)}"

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
            return response.strip() or "I'm here to help with more details!"
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
        q_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should']
        return any(text.lower().startswith(q) for q in q_words) or '?' in text

    def needs_summarization(self, text):
        return len(text.split()) > 50 or 'summarize' in text.lower()

    def get_knowledge_context(self, question):
        knowledge_base = {
            'business': "A business plan includes executive summary, market research, structure, funding, and more.",
            'technology': "Technology covers software, hardware, AI, development, and innovation.",
            'science': "Science is the systematic study of the physical and natural world.",
            'health': "Health refers to physical and mental well-being, lifestyle, and medical care.",
            'education': "Education is the process of learning and teaching knowledge and skills."
        }
        for topic, context in knowledge_base.items():
            if topic in question.lower():
                return context
        return "This is a general question requiring thoughtful analysis and knowledge."

    def fallback_response(self, prompt):
        if 'business plan' in prompt.lower():
            return (
                "Business Plan Structure:\n"
                "1. Executive Summary\n2. Market Analysis\n3. Products/Services\n"
                "4. Marketing Strategy\n5. Operations Plan\n6. Financial Projections"
            )
        elif 'code' in prompt.lower():
            return (
                "Coding Help:\nLanguages: Python, JavaScript\nTools: Flask, React, Git\n"
                "Topics: Web, APIs, Data Science, Mobile Apps"
            )
        else:
            return f"I see you're asking about: {prompt}. Let me help break it down."

# 🚀 Initialize AI engine
free_ai = FreeAIEngine()

# 🔌 Blueprint Loader
def inject_blueprint(path, bp_name, url_prefix):
    try:
        mod = __import__(path, fromlist=[bp_name])
        app.register_blueprint(getattr(mod, bp_name), url_prefix=url_prefix)
        print(f"✅ Injected {bp_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed: {path}.{bp_name}\n{traceback.format_exc()}")

# 🧠 Mythiq Modules (Updated with ai_proxy_bp)
modules = [
    ("branches.brain_orchestrator.routes", "brain_bp", "/api/brain"),
    ("branches.ai_router.routes", "ai_router_bp", "/api/ai"),
    ("branches.intent_router.routes", "intent_bp", "/api/intent"),
    ("branches.reasoning_engine.routes", "reasoning_bp", "/api/reason"),
    ("branches.docs.routes", "docs_bp", "/api/docs"),
    ("branches.ai_proxy.routes", "ai_proxy_bp", "/"),
]

# 🔁 Inject All Blueprints
for path, bp_name, prefix in modules:
    inject_blueprint(path, bp_name, prefix)

# 🌐 Root UI Page (⚠️ may conflict with ai_proxy_bp → `/`)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# 🧠 Brain API (Local AI)
@app.route('/api/brain', methods=['POST'])
def process_brain_request():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({
                'error': 'No prompt provided',
                'status': 'error',
                'timestamp': time.time()
            }), 400

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
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': time.time()
        }), 500

# 🧪 Health Check
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq Gateway Online",
        "timestamp": time.time()
    }), 200

# ⚙️ Boot the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
