from flask import Flask, jsonify, render_template
import os, time, traceback
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# 🔁 Initialize Flask App
app = Flask(__name__, static_url_path="/static")

# 🧠 Global healthcheck
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "boot": "complete",
        "timestamp": time.time()
    }), 200

# 🔌 Safe blueprint injector
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

# 🔗 Core modules
modules = [
    ("branches.brain_orchestrator.routes", "brain_bp", "/api/brain"),               # ✅ Working blueprint
    ("branches.self_learning.reflect_api", "reflect_bp", "/api/learn"),             # ✅ Reflective core
    ("branches.analytics_core.routes", "analytics_bp", "/api/analytics"),           # ✅ Trend monitor active
    ("branches.intent_router.intent_api", "intent_bp", "/api/intent"),
    ("branches.image_generator.routes", "image_bp", "/api/image"),
    ("branches.persona_settings.routes", "persona_bp", "/api/persona"),
    ("branches.context_propagator.context_api", "context_bp", "/api/context"),
    ("branches.task_executor.routes", "task_bp", "/api/dispatch"),
    ("branches.gallery_renderer.routes", "gallery_bp", "/api/gallery"),
    ("branches.dashboard_analytics.routes", "dashboard_bp", "/api/dashboard"),
    ("branches.dialogue_engine.routes", "dialogue_bp", "/api/chat"),
    ("branches.voice_interface.routes", "voice_bp", "/api/voice"),
    ("branches.agent_roles.routes", "agent_bp", "/api/role"),
    ("branches.self_tuning.routes", "tune_bp", "/api/tune"),
    ("branches.goal_engine.routes", "goal_bp", "/api/goal"),
    ("branches.knowledge_writer.routes", "writer_bp", "/api/write"),
    ("branches.semantic_search.routes", "search_bp", "/api/search"),
    ("branches.api_bridge.routes", "bridge_bp", "/api/bridge"),
    ("branches.action_router.routes", "action_bp", "/api/action"),
    ("branches.user_core.routes", "user_bp", "/api/user"),
    ("branches.experiment_lab.routes", "lab_bp", "/api/lab"),
    ("branches.train_assist.routes", "train_bp", "/api/train"),
    ("branches.story_maker.routes", "story_bp", "/api/story"),
    ("branches.adaptive_persona.routes", "persona_adapt_bp", "/api/persona/adapt"),
    ("branches.agent_mesh.routes", "mesh_bp", "/api/mesh"),
    ("branches.mobile_mode.routes", "mobile_bp", "/api/mobile"),
    ("branches.cognition_graph.routes", "graph_bp", "/api/graph"),
    ("branches.reflex_core.routes", "reflex_bp", "/api/reflex"),
    ("branches.memory_explorer.routes", "explorer_bp", "/api/memory/explore"),
    ("branches.secure_core.routes", "secure_bp", "/api/secure"),
    ("branches.language_router.routes", "lang_bp", "/api/lang"),
    ("branches.media_synth.routes", "media_bp", "/api/media"),
    ("branches.skill_meter.routes", "skill_bp", "/api/skill"),
    ("branches.world_context.routes", "context_world_bp", "/api/context"),
    ("branches.routine_designer.routes", "routine_bp", "/api/routine"),
    ("branches.imaginary_core.routes", "dream_bp", "/api/dream"),
    ("branches.commerce_agent.routes", "commerce_bp", "/api/commerce"),
    ("branches.learning_hive.routes", "hive_bp", "/api/train/assist"),
    ("branches.dialogue_memory.routes", "dialogue_memory_api", "/api/dialogue/memory"),
    ("branches.ethics_core.routes", "ethics_api", "/api/ethics/decision"),
    ("branches.exploration_api.routes", "explore_api", "/api/explore"),
    ("branches.meta_modeler.routes", "meta_api", "/api/meta/model"),
    ("branches.interface_core.routes", "interface_api", "/api/interface/style"),
    ("branches.rl_engine.routes", "rl_bp", "/api/rl"),
    ("branches.explain_core.routes", "explain_bp", "/api/explain"),
    ("branches.federated_core.routes", "fed_bp", "/api/federated"),
    ("branches.immersive_interface.routes", "imm_bp", "/api/immersive"),
    ("branches.bio_emotion.routes", "bio_bp", "/api/bio")
]

# 🚀 Inject modules
for path, bp_name, prefix in modules:
    inject_blueprint(path, bp_name, prefix)

# 📦 Root fallback
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html") if os.path.exists("templates/index.html") else jsonify({
        "message": "Welcome to Mythiq 🔥"
    })
