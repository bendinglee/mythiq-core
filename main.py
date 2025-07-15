from flask import Flask, jsonify, request
import os, time, traceback
from dotenv import load_dotenv

# 🔐 Load environment early
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
print("🚀 Mythiq ignition sequence started.")
print("  HF_TOKEN present:", bool(HF_TOKEN))
print("  WOLFRAM_APP_ID present:", bool(WOLFRAM_APP_ID))

# ✅ Initialize Flask app
app = Flask(__name__)

# 🩺 Healthcheck registered first
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "message": "Mythiq kernel alive",
        "timestamp": time.time()
    })

# 🔌 Blueprint injector (logs but never crashes)
def inject_blueprint(branch, module_file, attr_name, url_prefix):
    try:
        mod = __import__(f"branches.{branch}.{module_file}", fromlist=[attr_name])
        bp = getattr(mod, attr_name)
        app.register_blueprint(bp, url_prefix=url_prefix)
        print(f"✅ Injected: {branch} → {url_prefix}")
    except Exception:
        print(f"❌ Failed injecting {branch}:", traceback.format_exc())

# 🔗 All branches Phase 0–25
to_load = [
    # Core branches (0–15)
    ("brain_orchestrator", "brain_api",     "get_brain_blueprint", "/api/brain"),
    ("intent_router",      "intent_api",    "intent_bp",          "/api/intent"),
    ("self_learning",      "reflect_api",   "reflect_bp",         "/api/learn"),
    ("image_generator",    "routes",        "image_bp",           "/api/image"),
    ("persona_settings",   "routes",        "persona_bp",         "/api/persona"),
    ("context_propagator", "context_api",   "context_bp",         "/api/context"),
    ("task_executor",      "routes",        "task_bp",            "/api/dispatch"),
    ("gallery_renderer",   "routes",        "gallery_bp",         "/api/gallery"),
    ("dashboard_analytics","routes",        "dashboard_bp",       "/api/dashboard"),
    ("dialogue_engine",    "routes",        "dialogue_bp",        "/api/chat"),
    ("voice_interface",    "routes",        "voice_bp",           "/api/voice"),
    ("agent_roles",        "routes",        "agent_bp",           "/api/role"),
    ("self_tuning",        "routes",        "tune_bp",            "/api/tune"),
    ("goal_engine",        "routes",        "goal_bp",            "/api/goal"),
    ("knowledge_writer",   "routes",        "writer_bp",          "/api/write"),
    ("semantic_search",    "routes",        "search_bp",          "/api/search"),
    ("api_bridge",         "routes",        "bridge_bp",          "/api/bridge"),
    ("action_router",      "routes",        "action_bp",          "/api/action"),
    ("user_core",          "routes",        "user_bp",            "/api/user"),
    ("experiment_lab",     "routes",        "lab_bp",             "/api/lab"),
    ("train_assist",       "routes",        "train_bp",           "/api/train"),
    ("analytics_core",     "routes",        "analytics_bp",       "/api/analytics"),
    ("story_maker",        "routes",        "story_bp",           "/api/story"),
    ("adaptive_persona",   "routes",        "persona_adapt_bp",   "/api/persona/adapt"),
    ("agent_mesh",         "routes",        "mesh_bp",            "/api/mesh"),
    ("mobile_mode",        "routes",        "mobile_bp",          "/api/mobile"),
    ("cognition_graph",    "routes",        "graph_bp",           "/api/graph"),
    ("reflex_core",        "routes",        "reflex_bp",          "/api/reflex"),
    ("memory_explorer",    "routes",        "explorer_bp",        "/api/memory/explore"),
    ("secure_core",        "routes",        "secure_bp",          "/api/secure"),
    ("language_router",    "routes",        "lang_bp",            "/api/lang"),
    ("media_synth",        "routes",        "media_bp",           "/api/media"),
    ("skill_meter",        "routes",        "skill_bp",           "/api/skill"),
    ("world_context",      "routes",        "context_world_bp",   "/api/context"),
    ("routine_designer",   "routes",        "routine_bp",         "/api/routine"),
    ("imaginary_core",     "routes",        "dream_bp",           "/api/dream"),
    ("commerce_agent",     "routes",        "commerce_bp",        "/api/commerce"),
    ("learning_hive",      "routes",        "hive_bp",            "/api/train/assist"),
    # Phase 16–20
    ("dialogue_memory",    "routes",        "dialogue_memory_api","/api/dialogue/memory"),
    ("ethics_core",        "routes",        "ethics_api",         "/api/ethics/decision"),
    ("exploration_api",    "routes",        "explore_api",        "/api/explore"),
    ("meta_modeler",       "routes",        "meta_api",           "/api/meta/model"),
    ("interface_core",     "routes",        "interface_api",      "/api/interface/style"),
    # Phase 21–25
    ("rl_engine",          "routes",        "rl_bp",              "/api/rl"),
    ("explain_core",       "routes",        "explain_bp",         "/api/explain"),
    ("federated_core",     "routes",        "fed_bp",             "/api/federated"),
    ("immersive_interface","routes",        "imm_bp",             "/api/immersive"),
    ("bio_emotion",        "routes",        "bio_bp",             "/api/bio")
]

for branch, module_file, attr, prefix in to_load:
    inject_blueprint(branch, module_file, attr, prefix)

# 📦 Serve a simple UI (if you have one)
@app.route("/", methods=["GET"])
def index():
    return jsonify({ "message": "Welcome to Mythiq 🔥" })

# 🚀 Launch
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🚀 Launching Mythiq on port {port}")
    app.run(host="0.0.0.0", port=port)
