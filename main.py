from flask import Flask, jsonify, request
import time, os

app = Flask(__name__)

# 🔗 Branch: Brain Orchestrator
try:
    from branches.brain_orchestrator.brain_api import get_brain_blueprint
    app.register_blueprint(get_brain_blueprint(), url_prefix="/api/brain")
except Exception as e:
    print(f"❌ Brain orchestrator failed to inject: {e}")

# 🔗 Branch: Intent Router
try:
    from branches.intent_router.intent_api import intent_bp
    app.register_blueprint(intent_bp, url_prefix="/api/intent")
except Exception as e:
    print(f"❌ Intent router failed to inject: {e}")

# 🔗 Branch: Memory Core (optional blueprint if added)
# from branches.memory_core.routes import memory_bp
# app.register_blueprint(memory_bp, url_prefix="/api/memory")

# 🔗 Branch: Self Learning (optional blueprint if added)
# from branches.self_learning.learning_api import learning_bp
# app.register_blueprint(learning_bp, url_prefix="/api/learn")

# 🌐 Railway Healthcheck Endpoint
@app.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq cognitive kernel is alive ✅",
        "timestamp": time.time()
    })

# ✅ Live test route to reflect on session
@app.route("/api/reflect", methods=["GET"])
def reflect_live():
    from branches.brain_orchestrator.core_reflector import reflect_on_session
    return jsonify(reflect_on_session())

# 🚀 Launching App
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"✅ Mythiq launching on port {port}...")
    app.run(host="0.0.0.0", port=port)
