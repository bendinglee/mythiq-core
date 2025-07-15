from flask import Flask, jsonify
import os, time, traceback
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# 🚀 Initialize Flask App
app = Flask(__name__, static_url_path="/static")

# ⚡ Instant healthcheck for Railway
@app.route("/healthcheck", methods=["GET"])
def instant_check():
    return "OK", 200

# 🧠 Full system status check
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "boot": "complete",
        "timestamp": time.time()
    }), 200

# 🔌 Modular blueprint injector
def inject_blueprint(path, bp_name, url_prefix):
    try:
        mod = __import__(path, fromlist=[bp_name])
        app.register_blueprint(getattr(mod, bp_name), url_prefix=url_prefix)
        print(f"✅ Injected {bp_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed: {path}.{bp_name}\n{traceback.format_exc()}")

# ✅ Inject fallback status_core
try:
    from branches.status_core.routes import status_bp
    app.register_blueprint(status_bp)
    print("✅ status_core loaded")
except Exception:
    print("❌ status_core failed:", traceback.format_exc())

# 🔗 Inject all core branches
modules = [
    # 🔍 Cognition, Learning, Interaction
    ("branches.brain_orchestrator.routes", "brain_bp", "/api/brain"),
    ("branches.self_learning.reflect_api", "reflect_bp", "/api/learn"),
    ("branches.intent_router.intent_api", "intent_bp", "/api/intent"),
    ("branches.analytics_core.routes", "analytics_bp", "/api/analytics"),
    ("branches.image_generator.routes", "image_bp", "/api/image"),
    ("branches.voice_interface.routes", "voice_bp", "/api/voice"),
    ("branches.dialogue_engine.routes", "dialogue_bp", "/api/chat"),
    ("branches.dialogue_memory.routes", "dialogue_memory_api", "/api/dialogue/memory"),

    # 🎭 Personality & Goals
    ("branches.persona_settings.routes", "persona_bp", "/api/persona"),
    ("branches.adaptive_persona.routes", "persona_adapt_bp", "/api/persona/adapt"),
    ("branches.goal_engine.routes", "goal_bp", "/api/goal"),

    # 🧠 Introspection & System Identity
    ("branches.meta_modeler.routes", "meta_api", "/api/meta/model"),
    ("branches.memory_explorer.routes", "explorer_bp", "/api/memory/explore"),
    ("branches.api_docs.swagger", "docs_bp", "/api/docs"),
    ("branches.api_docs.openapi", "swagger_bp", "/api"),
    ("system_introspect.bootmap", "bootmap_api", "/api/system"),
    ("system_introspect.diagnostics", "diagnostics_api", "/api/diagnostics"),
    ("system_introspect.reload", "reload_api", "/api"),
    ("system_introspect.uptime", "uptime_api", "/api/uptime"),

    # 🔄 Actions, Routing, Reflection
    ("branches.api_bridge.routes", "bridge_bp", "/api/bridge"),
    ("branches.action_router.routes", "action_bp", "/api/action"),
    ("branches.reflex_core.routes", "reflex_bp", "/api/reflex"),
    ("branches.self_tuning.routes", "tune_bp", "/api/tune"),
    ("branches.task_executor.routes", "task_bp", "/api/dispatch"),
    ("branches.routine_designer.routes", "routine_bp", "/api/routine"),

    # 🧬 Knowledge, Writing, Search
    ("branches.semantic_search.routes", "search_bp", "/api/search"),
    ("branches.knowledge_writer.routes", "writer_bp", "/api/write"),
    ("branches.explain_core.routes", "explain_bp", "/api/explain"),

    # 🧑‍🔧 User, Role, Interfaces
    ("branches.agent_roles.routes", "agent_bp", "/api/role"),
    ("branches.user_core.routes", "user_bp", "/api/user"),
    ("branches.interface_core.routes", "interface_api", "/api/interface/style"),
    ("branches.immersive_interface.routes", "imm_bp", "/api/immersive"),

    # 🔒 Safety, Emotion, Language
    ("branches.secure_core.routes", "secure_bp", "/api/secure"),
    ("branches.ethics_core.routes", "ethics_api", "/api/ethics/decision"),
    ("branches.language_router.routes", "lang_bp", "/api/lang"),
    ("branches.bio_emotion.routes", "bio_bp", "/api/bio"),

    # ⚡ Visualization & Story
    ("branches.gallery_renderer.routes", "gallery_bp", "/api/gallery"),
    ("branches.story_maker.routes", "story_bp", "/api/story"),
    ("branches.media_synth.routes", "media_bp", "/api/media"),
    ("branches.imaginary_core.routes", "dream_bp", "/api/dream"),

    # 📊 Dashboards, Mesh, Mobile
    ("branches.dashboard_analytics.routes", "dashboard_bp", "/api/dashboard"),
    ("branches.agent_mesh.routes", "mesh_bp", "/api/mesh"),
    ("branches.mobile_mode.routes", "mobile_bp", "/api/mobile"),
    ("branches.federated_core.routes", "fed_bp", "/api/federated"),

    # 🧪 Experimental Modules
    ("branches.experiment_lab.routes", "lab_bp", "/api/lab"),
    ("branches.exploration_api.routes", "explore_api", "/api/explore"),

    # 📚 Training & Scaling
    ("branches.train_assist.routes", "train_bp", "/api/train"),
    ("branches.learning_hive.routes", "hive_bp", "/api/train/assist"),
    ("branches.skill_meter.routes", "skill_bp", "/api/skill"),

    # 🛍️ Commerce
    ("branches.commerce_agent.routes", "commerce_bp", "/api/commerce"),

    # 🧠 Context & RL
    ("branches.context_propagator.context_api", "context_bp", "/api/context"),
    ("branches.rl_engine.routes", "rl_bp", "/api/rl"),
    ("branches.cognition_graph.routes", "graph_bp", "/api/graph")
]

# 🚀 Inject modules dynamically
for path, bp_name, prefix in modules:
    inject_blueprint(path, bp_name, prefix)

# 📦 Root index
@app.route("/", methods=["GET"])
def index():
    return jsonify({ "message": "Welcome to Mythiq 🔥" })
