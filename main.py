from flask import Flask, jsonify, request
import time, os

app = Flask(__name__)

# ✅ Dynamic blueprint injection
def inject_blueprint(branch, filename, handler_name, url_prefix):
    try:
        module = __import__(f"branches.{branch}.{filename}", fromlist=[handler_name])
        handler = getattr(module, handler_name)
        app.register_blueprint(handler, url_prefix=url_prefix)
        print(f"✅ {branch} injected → {url_prefix}")
    except Exception as e:
        print(f"❌ {branch} failed: {e}")

# ✅ Inject all branch blueprints
modules = [
    ("brain_orchestrator", "brain_api", "get_brain_blueprint", "/api/brain"),
    ("intent_router", "intent_api", "intent_bp", "/api/intent"),
    ("self_learning", "reflect_api", "reflect_bp", "/api/learn"),
    ("image_generator", "routes", "image_bp", "/api/image"),
    ("persona_settings", "routes", "persona_bp", "/api/persona"),
    ("context_propagator", "context_api", "context_bp", "/api/context"),
    ("task_executor", "routes", "task_bp", "/api/dispatch"),
    ("gallery_renderer", "routes", "gallery_bp", "/api/gallery"),
    ("dashboard_analytics", "routes", "dashboard_bp", "/api/dashboard"),
    ("dialogue_engine", "routes", "dialogue_bp", "/api/chat"),
    ("voice_interface", "routes", "voice_bp", "/api/voice"),
    ("agent_roles", "routes", "agent_bp", "/api/role"),
    ("self_tuning", "routes", "tune_bp", "/api/tune"),
    ("goal_engine", "routes", "goal_bp", "/api/goal"),
    ("knowledge_writer", "routes", "writer_bp", "/api/write"),
    ("semantic_search", "routes", "search_bp", "/api/search"),
    ("api_bridge", "routes", "bridge_bp", "/api/bridge"),
    ("action_router", "routes", "action_bp", "/api/action"),
    ("user_core", "routes", "user_bp", "/api/user"),
    ("experiment_lab", "routes", "lab_bp", "/api/lab"),
    ("train_assist", "routes", "train_bp", "/api/train"),
    ("analytics_core", "routes", "analytics_bp", "/api/analytics"),
    ("story_maker", "routes", "story_bp", "/api/story")
]

for branch, file, handler, prefix in modules:
    inject_blueprint(branch, file, handler, prefix)

# ✅ Independent direct route: memory_core reflection
try:
    from branches.memory_core.reflect import generate_summary
    @app.route("/api/memory/reflect", methods=["GET"])
    def memory_reflect():
        return jsonify(generate_summary())
    print("✅ memory_core reflection route enabled")
except Exception as e:
    print(f"❌ memory_core reflect route failed: {e}")

# ✅ Offline cache sync endpoint
try:
    from branches.offline_cache.colab_sync import sync_with_colab
    @app.route("/api/cache/sync", methods=["GET"])
    def sync_cache():
        repo_url = request.args.get("repo", "")
        result = sync_with_colab(repo_url)
        return jsonify(result)
    print("✅ offline cache sync route enabled")
except Exception as e:
    print(f"❌ offline_cache sync failed: {e}")

# ✅ Healthcheck for Railway deployment
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "message": "Mythiq kernel alive",
        "timestamp": time.time()
    })

# ✅ Launch application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Launching Mythiq on port {port}")
    app.run(host="0.0.0.0", port=port)
