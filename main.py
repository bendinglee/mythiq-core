from flask import Flask, jsonify
import os, time, traceback
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

# 🚀 Initialize Flask App
app = Flask(__name__, static_url_path="/static")

# ⚡ Railway healthcheck
@app.route("/healthcheck", methods=["GET"])
def instant_check():
    return "OK", 200

# 🧠 Global system status
@app.route("/api/status", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok",
        "boot": "complete",
        "timestamp": time.time()
    }), 200

# 🔌 Blueprint injector
def inject_blueprint(path, bp_name, url_prefix):
    try:
        mod = __import__(path, fromlist=[bp_name])
        app.register_blueprint(getattr(mod, bp_name), url_prefix=url_prefix)
        print(f"✅ Injected {bp_name} → {url_prefix}")
    except Exception:
        print(f"❌ Failed: {path}.{bp_name}\n{traceback.format_exc()}")

# ✅ Fallback route
try:
    from branches.status_core.routes import status_bp
    app.register_blueprint(status_bp)
    print("✅ status_core loaded")
except Exception:
    print("❌ status_core failed:", traceback.format_exc())

# 🔗 Inject All Modules — Phase I–XXX
modules = [

    # ⚙️ Core Modules
    ("branches/api_docs.routes", "docs_bp", "/api/docs"),
    ("branches/api_docs.openapi", "swagger_bp", "/api"),
    ("branches/api_docs.swagger", "docs_bp", "/api/docs"),
    ("branches.brain_orchestrator.routes", "brain_bp", "/api/brain"),
    ("branches.self_learning.reflect_api", "reflect_bp", "/api/learn"),
    ("branches.intent_router.intent_api", "intent_bp", "/api/intent"),
    ("branches.dialogue_engine.routes", "dialogue_bp", "/api/chat"),
    ("branches.dialogue_engine.chat_stream", "stream_bp", "/api/chat"),
    ("branches.dialogue_memory.routes", "dialogue_memory_api", "/api/dialogue/memory"),
    ("branches.memory_explorer.routes", "explorer_bp", "/api/memory/explore"),
    ("branches.adaptive_persona.routes", "persona_adapt_bp", "/api/persona/adapt"),
    ("branches.persona_settings.routes", "persona_bp", "/api/persona"),
    ("branches.meta_modeler.routes", "meta_api", "/api/meta/model"),
    ("branches.semantic_search.routes", "search_bp", "/api/search"),
    ("branches.explain_core.routes", "explain_bp", "/api/explain"),
    ("branches.knowledge_writer.routes", "writer_bp", "/api/write"),
    ("branches.voice_interface.routes", "voice_bp", "/api/voice"),
    ("branches.analytics_core.routes", "analytics_bp", "/api/analytics"),
    ("branches.analytics_core.feedback", "feedback_api", "/api/analytics"),
    ("branches.image_generator.routes", "image_bp", "/api/image"),
    ("branches.media_synth.routes", "media_bp", "/api/media"),
    ("branches.imaginary_core.routes", "dream_bp", "/api/dream"),
    ("branches.gallery_renderer.routes", "gallery_bp", "/api/gallery"),
    ("branches.story_maker.routes", "story_bp", "/api/story"),
    ("branches.goal_engine.routes", "goal_bp", "/api/goal"),
    ("branches.goal_engine.reward", "reward_bp", "/api/goal"),
    ("branches.reflex_core.routes", "reflex_bp", "/api/reflex"),
    ("branches.task_executor.routes", "task_bp", "/api/dispatch"),
    ("branches.task_executor.feedback", "feedback_bp", "/api/dispatch"),
    ("branches.routine_designer.routes", "routine_bp", "/api/routine"),

    # 🧑 Agent & Interface
    ("branches.interface_core.routes", "interface_api", "/api/interface/style"),
    ("branches.agent_roles.routes", "agent_bp", "/api/role"),
    ("branches.agent_mesh.routes", "mesh_bp", "/api/mesh"),
    ("branches.user_core.routes", "user_bp", "/api/user"),
    ("branches.immersive_interface.routes", "imm_bp", "/api/immersive"),
    ("branches.mobile_mode.routes", "mobile_bp", "/api/mobile"),

    # 🔍 Security, Ethics & Exploration
    ("branches.experiment_lab.routes", "lab_bp", "/api/lab"),
    ("branches.exploration_api.routes", "explore_api", "/api/explore"),
    ("branches.secure_core.routes", "secure_bp", "/api/secure"),
    ("branches.ethics_core.routes", "ethics_api", "/api/ethics/decision"),
    ("branches.bio_emotion.routes", "bio_bp", "/api/bio"),
    ("branches.language_router.routes", "lang_bp", "/api/lang"),

    # 🛒 Commerce & Skills
    ("branches.commerce_agent.routes", "commerce_bp", "/api/commerce"),
    ("branches.train_assist.routes", "train_bp", "/api/train"),
    ("branches.learning_hive.routes", "hive_bp", "/api/train/assist"),
    ("branches.skill_meter.routes", "skill_bp", "/api/skill"),

    # 🔁 Context & System Intelligence
    ("branches.context_propagator.context_api", "context_bp", "/api/context"),
    ("branches.cognition_graph.routes", "graph_bp", "/api/graph"),
    ("branches.rl_engine.routes", "rl_bp", "/api/rl"),
    ("branches.api_bridge.routes", "bridge_bp", "/api/bridge"),
    ("branches.action_router.routes", "action_bp", "/api/action"),

    # 🌍 Social + Ethics
    ("branches.culture_core.routes", "culture_bp", "/api/culture"),
    ("branches.bonding_engine.routes", "bond_bp", "/api/social"),
    ("branches.ethics_dialogue.routes", "ethics_bp", "/api/discourse"),

    # 🧬 Introspection & Fallback
    ("branches.introspect_core.routes", "introspect_bp", "/api/self"),
    ("branches.intent_audit.routes", "intent_bp", "/api/intent"),
    ("branches.fault_map.routes", "fault_bp", "/api/error"),

    # 🧠 Cognitive Modeling
    ("branches.memory_fusion.routes", "fuse_bp", "/api/memory"),
    ("branches.neurostyle_engine.routes", "sculpt_bp", "/api/cognition"),
    ("branches.recall_weight.routes", "weight_bp", "/api/recall"),
    ("branches.voice_identity.routes", "voice_bp", "/api/voice"),
    ("branches.persona_projection.routes", "modecast_bp", "/api/persona"),
    ("branches.audio_emotion.routes", "audio_bp", "/api/audio"),

    # 🤖 Agent Mesh & Feedback
    ("branches.agent_mesh_builder.routes", "cluster_bp", "/api/agents"),
    ("branches.agent_synchronizer.routes", "sync_bp", "/api/agents"),
    ("branches.mesh_mapper.routes", "mesh_bp", "/api/mesh"),
    ("branches.rl_studio.routes", "train_bp", "/api/train"),
    ("branches.goal_refactor.routes", "adapt_bp", "/api/goal"),
    ("branches.reflex_mutator.routes", "mutate_bp", "/api/reflex"),

    # 📦 Plugin Ecosystem
    ("branches.plugin_installer.routes", "install_bp", "/api/plugin"),
    ("branches.plugin_finder.routes", "finder_bp", "/api/plugin"),
    ("branches.plugin_rating.routes", "rating_bp", "/api/plugin"),

    # 📡 Network Sync
    ("branches.uptime_sync.routes", "network_bp", "/api/status"),
    ("branches.agent_uptime.routes", "agentlive_bp", "/api/status"),
    ("branches.mission_sync.routes", "mission_bp", "/api/status"),

    # 🧠 Emotional Continuity
    ("branches.story_emotion.routes", "emotion_bp", "/api/narrative"),
    ("branches.timeline_persistence.routes", "echo_bp", "/api/memory"),
    ("branches.persona_growth.routes", "growth_bp", "/api/persona"),

    # 🚀 Singularity Activation
    ("branches.singularity_switch.routes", "ignite_bp", "/api/mesh"),
    ("branches.agent_merge.routes", "merge_bp", "/api/agents"),
    ("branches.ai_online.routes", "online_bp", "/api/intelligence"),

    # 🧠 Phase XXI–XXX Additions
    ("branches.experience_modeler.routes", "experience_bp", "/api/experience"),
    ("branches.user_feedback_fusion.routes", "feedback_bp_userfusion", "/api/user"),
   ("branches.persona_bond_engine.routes", "bond_bp_persona", "/api/user/persona"),
    ("branches.mesh_dialogue_engine.routes", "meshchat_bp", "/api/chat"),
        ("branches.symbolic_context_engine.routes", "symbol_bp", "/api/symbol"),
    ("branches.visual_storymaker.routes", "visualstory_bp", "/api/narrative"),
    ("branches.api_extension_bridge.routes", "bridge_bp", "/api/bridge"),
    ("branches.sentient_core.routes", "sentient_bp", "/api/cognition")
]  # ← 🟢 IMPORTANT: Closes the modules list properly

# 🚀 Inject all modules
for path, bp_name, prefix in modules:
    inject_blueprint(path, bp_name, prefix)

# 🏁 Root fallback route
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to Mythiq 🔥",
        "phases": "I–XXX active",
        "timestamp": time.time()
    })
