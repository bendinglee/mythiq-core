from flask import Flask, request, jsonify, render_template
import os, traceback
from dotenv import load_dotenv

# 🔐 Environment setup
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

print("🚀 Mythiq ignition sequence started.")
print("HF_TOKEN present:", bool(HF_TOKEN))
print("WOLFRAM_APP_ID present:", bool(WOLFRAM_APP_ID))

# ✅ Initialize Flask
app = Flask(__name__, static_url_path="/static")

# 🔁 Dynamic module injection
try:
    from branches import init_modules
    init_modules(app)
    print("🔄 Dynamic modules loaded.")
except Exception as e:
    print("❌ Module injection failed:", traceback.format_exc())

# 🔗 Blueprint registration
try:
    # 📦 Core + Phase 0–15 (abbreviated)
    from branches.brain_orchestrator.routes import brain_api
    from branches.intent_engine.routes import intent_api
    from branches.image_generator.routes import generate_image_route
    from branches.persona_settings.routes import persona_api
    from branches.dashboard_viewer.routes import dashboard_api
    from branches.dialogue_engine.routes import dialogue_api
    app.register_blueprint(brain_api)
    app.register_blueprint(intent_api)
    app.register_blueprint(persona_api)
    app.register_blueprint(dashboard_api)
    app.register_blueprint(dialogue_api)

    # 🧠 Phase 16–20 additions
    from branches.dialogue_memory.routes import dialogue_memory_api
    from branches.ethics_core.routes import ethics_api
    from branches.exploration_api.routes import explore_api
    from branches.meta_modeler.routes import meta_api
    from branches.interface_core.routes import interface_api
    app.register_blueprint(dialogue_memory_api, url_prefix="/api/dialogue/memory")
    app.register_blueprint(ethics_api, url_prefix="/api/ethics/decision")
    app.register_blueprint(explore_api, url_prefix="/api/explore")
    app.register_blueprint(meta_api, url_prefix="/api/meta/model")
    app.register_blueprint(interface_api, url_prefix="/api/interface/style")

    print("✅ Phase 16–20 injected.")
except Exception as e:
    print("❌ Phase injection failed:", traceback.format_exc())

# 🌐 API endpoints
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq kernel fully deployed ✅",
        "timestamp": os.times()
    })

@app.route("/api/generate-image", methods=["POST"])
def generate_image():
    return generate_image_route()

@app.route("/")
def index():
    return render_template("index.html")

# 🧠 Final Launch
print("🎯 Mythiq operational — launching Flask...")

if __name__ == "__main__":
    print("🟢 Running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
