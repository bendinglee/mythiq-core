
 from flask import Flask, jsonify, request
import time, os

app = Flask(__name__)

# 🚀 Phase Injection Map
module_map = [
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

# 🔌 Dynamic Blueprint Injector
for branch, file, handler, url in module_map:
    try:
        exec(f"from branches.{branch}.{file} import {handler}")
        exec(f"app.register_blueprint({handler}, url_prefix='{url}')")
        print(f"✅ {branch} injected.")
    except Exception as e:
        print(f"❌ {branch} error: {e}")

# 🧠 Memory Reflection (direct route)
try:
    from branches.memory_core.reflect import generate_summary
    @app.route("/api/memory/reflect", methods=["GET"])
    def reflect_memory():
        return jsonify(generate_summary())
    print("✅ Memory reflection route registered.")
except Exception as e:
    print(f"❌ Memory core reflection error: {e}")

# 📦 Offline Cache Sync
try:
    from branches.offline_cache.colab_sync import sync_with_colab
    @app.route("/api/cache/sync", methods=["GET"])
    def sync_cache():
        repo_url = request.args.get("repo", "")
        return jsonify(sync_with_colab(repo_url))
    print("✅ Offline cache sync route registered.")
except Exception as e:
    print(f"❌ Offline cache sync error: {e}")

# 🌐 Healthcheck
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq is fully deployed and cognitively complete",
        "timestamp": time.time()
    })

# 🧠 Launch Kernel
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Mythiq launching on port {port}")
    app.run(host="0.0.0.0", port=port)
