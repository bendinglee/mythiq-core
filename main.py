from flask import Flask, jsonify, request
import time, os

app = Flask(__name__)

# 🔗 Brain Orchestrator
try:
    from branches.brain_orchestrator.brain_api import get_brain_blueprint
    app.register_blueprint(get_brain_blueprint(), url_prefix="/api/brain")
    print("✅ Brain orchestrator injected.")
except Exception as e:
    print(f"❌ Failed to inject brain orchestrator: {e}")

# 🔗 Intent Router
try:
    from branches.intent_router.intent_api import intent_bp
    app.register_blueprint(intent_bp, url_prefix="/api/intent")
    print("✅ Intent router injected.")
except Exception as e:
    print(f"❌ Failed to inject intent router: {e}")

# 🔗 Memory Core Reflection API
try:
    from branches.memory_core.reflect import generate_summary
    @app.route("/api/memory/reflect", methods=["GET"])
    def reflect_memory():
        return jsonify(generate_summary())
    print("✅ Memory core reflection route registered.")
except Exception as e:
    print(f"❌ Failed to register memory core reflect route: {e}")

# 🔗 Self-Learning Reflection API
try:
    from branches.self_learning.reflect_api import reflect_bp
    app.register_blueprint(reflect_bp, url_prefix="/api/learn")
    print("✅ Self-learning blueprint injected.")
except Exception as e:
    print(f"❌ Failed to inject self-learning: {e}")

# 🔗 Image Generator
try:
    from branches.image_generator.routes import image_bp
    app.register_blueprint(image_bp, url_prefix="/api/image")
    print("✅ Image generator injected.")
except Exception as e:
    print(f"❌ Failed to inject image generator: {e}")

# 🌐 Healthcheck Endpoint
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq kernel fully deployed",
        "timestamp": time.time()
    })

# 🚀 Launch
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Mythiq launching on port {port}")
    app.run(host="0.0.0.0", port=port)
