from flask import Flask, jsonify, request
import time, os

app = Flask(__name__)

# 🔌 Modular loader
def inject_blueprint(branch, filename, handler_name, url_prefix):
    try:
        module = __import__(f"branches.{branch}.{filename}", fromlist=[handler_name])
        handler = getattr(module, handler_name)
        app.register_blueprint(handler, url_prefix=url_prefix)
        print(f"✅ Injected: {branch} → {url_prefix}")
    except Exception as e:
        print(f"❌ Failed: {branch} → {e}")

# 🔗 Core + Phase 1–15 branches
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
    ("story_maker", "routes", "story_bp", "/api/story"),
    ("adaptive_persona", "routes", "persona_adapt_bp", "/api/persona/adapt"),
    ("agent_mesh", "routes", "mesh_bp", "/api/mesh"),
    ("mobile_mode", "routes", "mobile_bp", "/api/mobile"),
    ("cognition_graph", "routes", "graph_bp", "/api/graph"),
    ("reflex_core", "routes", "reflex_bp", "/api/reflex"),
    ("memory_explorer", "routes", "explorer_bp", "/api/memory/explore"),
    ("secure_core", "routes", "secure_bp", "/api/secure"),
    ("language_router", "routes", "lang_bp", "/api/lang"),
    ("media_synth", "routes", "media_bp", "/api/media"),
    ("skill_meter", "routes", "skill_bp", "/api/skill"),
    ("world_context", "routes", "context_world_bp", "/api/context"),
    ("routine_designer", "routes", "routine_bp", "/api/routine"),
    ("imaginary_core", "routes", "dream_bp", "/api/dream"),
    ("commerce_agent", "routes", "commerce_bp", "/api/commerce"),
    ("learning_hive", "routes", "hive_bp", "/api/train/assist")
]

for branch, file, handler, prefix in modules:
    inject_blueprint(branch, file, handler, prefix)

# 🧠 Memory summary direct endpoint
try:
    from branches.memory_core.reflect import generate_summary
    @app.route("/api/memory/reflect", methods=["GET"])
    def reflect_memory():
        return jsonify(generate_summary())
    print("✅ memory_core reflection route active")
except Exception as e:
    print(f"❌ memory_core reflection route failed: {e}")

# 🔄 Offline cache sync
try:
    from branches.offline_cache.colab_sync import sync_with_colab
    @app.route("/api/cache/sync", methods=["GET"])
    def sync_cache():
        repo_url = request.args.get("repo", "")
        result = sync_with_colab(repo_url)
        return jsonify(result)
    print("✅ offline_cache sync enabled")
except Exception as e:
    print(f"❌ offline_cache sync failed: {e}")

# 🩺 Healthcheck
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "message": "Mythiq is fully operational 🔥",
        "timestamp": time.time()
    })

# 🚀 Kernel launcher
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🚀 Mythiq launching on port {port}")
    app.run(host="0.0.0.0", port=port)
