from flask import Flask, jsonify
import os, time, traceback
from dotenv import load_dotenv

# 🔐 Environment setup
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# 🚀 Initialize Flask
app = Flask(__name__, static_url_path="/static")

# ⚡ Fast healthcheck for Railway
@app.route("/healthcheck", methods=["GET"])
def instant_check():
    return "OK", 200

# 🧠 Introspective healthcheck
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "boot": "complete",
        "timestamp": time.time()
    }), 200

# 🔌 Blueprint injector
def inject_blueprint(path, bp_name, url_prefix):
    try:
        mod = __import__(path, fromlist=[bp_name])
        app.register_blueprint(getattr(mod, bp_name), url_prefix=url_prefix)
        print(f"✅ Injected {bp_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed: {path}.{bp_name}\n{traceback.format_exc()}")

# ✅ Fallback core
try:
    from branches.status_core.routes import status_bp
    app.register_blueprint(status_bp)
    print("✅ status_core loaded")
except Exception:
    print("❌ status_core failed:", traceback.format_exc())

# 🔗 Modular cognition branches
modules = [
    # 🔍 Core cognition
    ("branches.brain_orchestrator.routes", "brain_bp", "/api/brain"),
    ("branches.self_learning.reflect_api", "reflect_bp", "/api/learn"),
    ("branches.intent_router.intent_api", "intent_bp", "/api/intent"),

    # 🧬 Introspection & memory
    ("branches.meta_modeler.routes", "meta_api", "/api/meta/model"),
    ("branches.memory_explorer.routes", "explorer_bp", "/api/memory/explore"),

    # 📚 Public route docs
    ("branches.api_docs.swagger", "docs_bp", "/api/docs"),

    # 🧠 Additional modules (already wired)
    # Keep existing paths as needed...
]

# 🧠 Inject all modules
for path, bp_name, prefix in modules:
    inject_blueprint(path, bp_name, prefix)

# 🏁 Welcome fallback
@app.route("/", methods=["GET"])
def index():
    return jsonify({ "message": "Welcome to Mythiq 🔥" })
