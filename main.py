from flask import Flask, jsonify, request, render_template
import os
import time
import traceback
from dotenv import load_dotenv

# 🩺 Healthcheck FIRST before any imports
app = Flask(__name__, static_url_path="/static")

@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "timestamp": time.time()
    }), 200

# 🔐 Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

print("🚀 Mythiq ignition sequence started.")
print("  HF_TOKEN present:", bool(HF_TOKEN))
print("  WOLFRAM_APP_ID present:", bool(WOLFRAM_APP_ID))

# 🔌 Safely inject all blueprints (Phase 0–25)
def inject_blueprint(module_path, blueprint_name, url_prefix):
    try:
        module = __import__(module_path, fromlist=[blueprint_name])
        bp = getattr(module, blueprint_name)
        app.register_blueprint(bp, url_prefix=url_prefix)
        print(f"✅ Injected {blueprint_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed injecting {module_path}.{blueprint_name}:\n", traceback.format_exc())

modules = [
    ("branches.brain_orchestrator.brain_api",     "get_brain_blueprint", "/api/brain"),
    ("branches.intent_router.intent_api",         "intent_bp",           "/api/intent"),
    ("branches.self_learning.reflect_api",        "reflect_bp",          "/api/learn"),
    ("branches.image_generator.routes",           "image_bp",            "/api/image"),
    ("branches.persona_settings.routes",          "persona_bp",          "/api/persona"),
    ("branches.context_propagator.context_api",   "context_bp",          "/api/context"),
    ("branches.task_executor.routes",             "task_bp",             "/api/dispatch"),
    ("branches.gallery_renderer.routes",          "gallery_bp",          "/api/gallery"),
    ("branches.dashboard_analytics.routes",       "dashboard_bp",        "/api/dashboard"),
    ("branches.dialogue_engine.routes",           "dialogue_bp",         "/api/chat"),
    ("branches.voice_interface.routes",           "voice_bp",            "/api/voice"),
    ("branches.agent_roles.routes",               "agent_bp",            "/api/role"),
    ("branches.self_tuning.routes",               "tune_bp",             "/api/tune"),
    ("branches.goal_engine.routes",               "goal_bp",             "/api/goal"),
    ("branches.knowledge_writer.routes",          "writer_bp",           "/api/write"),
    ("branches.semantic_search.routes",           "search_bp",           "/api/search"),
    ("branches.api_bridge.routes",                "bridge_bp",           "/api/bridge"),
    ("branches.action_router.routes",             "action_bp",           "/api/action"),
    ("branches.user_core.routes",                 "user_bp",             "/api/user"),
    ("branches.experiment_lab.routes",            "lab_bp",              "/api/lab"),
    ("branches.train_assist.routes",              "train_bp",            "/api/train"),
    ("branches.analytics_core.routes",            "analytics_bp",        "/api/analytics"),
    ("branches.story_maker.routes",               "story_bp",            "/api/story"),

    # Phases 11–15
    ("branches.adaptive_persona.routes",          "persona_adapt_bp",    "/api/persona/adapt"),
    ("branches.agent_mesh.routes",                "mesh_bp",             "/api/mesh"),
    ("branches.mobile_mode.routes",               "mobile_bp",           "/api/mobile"),
    ("branches.cognition_graph.routes",           "graph_bp",            "/api/graph"),
    ("branches.reflex_core.routes",               "reflex_bp",           "/api/reflex"),
    ("branches.memory_explorer.routes",           "explorer_bp",         "/api/memory/explore"),
    ("branches.secure_core.routes",               "secure_bp",           "/api/secure"),
    ("branches.language_router.routes",           "lang_bp",             "/api/lang"),
    ("branches.media_synth.routes",               "media_bp",            "/api/media"),
    ("branches.skill_meter.routes",               "skill_bp",            "/api/skill"),
    ("branches.world_context.routes",             "context_world_bp",    "/api/context"),
    ("branches.routine_designer.routes",          "routine_bp",          "/api/routine"),
    ("branches.imaginary_core.routes",            "dream_bp",            "/api/dream"),
    ("branches.commerce_agent.routes",            "commerce_bp",         "/api/commerce"),
    ("branches.learning_hive.routes",             "hive_bp",             "/api/train/assist"),

    # Phases 16–20
    ("branches.dialogue_memory.routes",           "dialogue_memory_api", "/api/dialogue/memory"),
    ("branches.ethics_core.routes",               "ethics_api",          "/api/ethics/decision"),
    ("branches.exploration_api.routes",           "explore_api",         "/api/explore"),
    ("branches.meta_modeler.routes",              "meta_api",            "/api/meta/model"),
    ("branches.interface_core.routes",            "interface_api",       "/api/interface/style"),

    # Phases 21–25
    ("branches.rl_engine.routes",                 "rl_bp",               "/api/rl"),
    ("branches.explain_core.routes",              "explain_bp",          "/api/explain"),
    ("branches.federated_core.routes",            "fed_bp",              "/api/federated"),
    ("branches.immersive_interface.routes",       "imm_bp",              "/api/immersive"),
    ("branches.bio_emotion.routes",               "bio_bp",              "/api/bio")
]

for path, handler, prefix in modules:
    inject_blueprint(path, handler, prefix)

# 📦 Optional root page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html") if os.path.exists("templates/index.html") else jsonify({ "message": "Welcome to Mythiq 🔥" })

# 🚀 Final launch
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🟢 Launching Mythiq on port {port}")
    app.run(host="0.0.0.0", port=port)
