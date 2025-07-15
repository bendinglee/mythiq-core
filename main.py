from flask import Flask, jsonify, request
import time, os

app = Flask(__name__)

# 🧠 Brain Orchestrator
try:
    from branches.brain_orchestrator.brain_api import get_brain_blueprint
    app.register_blueprint(get_brain_blueprint(), url_prefix="/api/brain")
    print("✅ Brain orchestrator injected.")
except Exception as e:
    print(f"❌ Brain orchestrator error: {e}")

# 🧭 Intent Router
try:
    from branches.intent_router.intent_api import intent_bp
    app.register_blueprint(intent_bp, url_prefix="/api/intent")
    print("✅ Intent router injected.")
except Exception as e:
    print(f"❌ Intent router error: {e}")

# 🧠 Memory Core Reflection
try:
    from branches.memory_core.reflect import generate_summary
    @app.route("/api/memory/reflect", methods=["GET"])
    def reflect_memory():
        return jsonify(generate_summary())
    print("✅ Memory reflection route registered.")
except Exception as e:
    print(f"❌ Memory core reflect route error: {e}")

# 🎯 Self-Learning Reflection
try:
    from branches.self_learning.reflect_api import reflect_bp
    app.register_blueprint(reflect_bp, url_prefix="/api/learn")
    print("✅ Self-learning blueprint injected.")
except Exception as e:
    print(f"❌ Self-learning error: {e}")

# 🎨 Image Generator
try:
    from branches.image_generator.routes import image_bp
    app.register_blueprint(image_bp, url_prefix="/api/image")
    print("✅ Image generator injected.")
except Exception as e:
    print(f"❌ Image generator error: {e}")

# 🧬 Persona Settings
try:
    from branches.persona_settings.routes import persona_bp
    app.register_blueprint(persona_bp, url_prefix="/api/persona")
    print("✅ Persona engine injected.")
except Exception as e:
    print(f"❌ Persona engine error: {e}")

# 🔗 Context Propagator
try:
    from branches.context_propagator.context_api import context_bp
    app.register_blueprint(context_bp, url_prefix="/api/context")
    print("✅ Context stitching injected.")
except Exception as e:
    print(f"❌ Context engine error: {e}")

# 🚀 Task Executor
try:
    from branches.task_executor.routes import task_bp
    app.register_blueprint(task_bp, url_prefix="/api/dispatch")
    print("✅ Task executor injected.")
except Exception as e:
    print(f"❌ Task executor error: {e}")

# 📦 Offline Cache
try:
    from branches.offline_cache.colab_sync import sync_with_colab
    @app.route("/api/cache/sync", methods=["GET"])
    def sync_cache():
        url = request.args.get("repo", "")
        result = sync_with_colab(url)
        return jsonify(result)
    print("✅ Offline cache sync route registered.")
except Exception as e:
    print(f"❌ Offline cache error: {e}")

# 🖼️ Gallery Renderer
try:
    from branches.gallery_renderer.routes import gallery_bp
    app.register_blueprint(gallery_bp, url_prefix="/api/gallery")
    print("✅ Gallery renderer injected.")
except Exception as e:
    print(f"❌ Gallery renderer error: {e}")

# 🌐 Healthcheck
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq kernel deployed",
        "timestamp": time.time()
    })

# 🚀 Launch
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Mythiq launching on port {port}")
    app.run(host="0.0.0.0", port=port)
