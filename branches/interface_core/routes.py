from flask import Blueprint, jsonify

# 🎨 Interface styling & plugin spec blueprint
interface_api = Blueprint("interface_api", __name__)

# ✅ Ping route for interface module status
@interface_api.route("/style/ping", methods=["GET"])
def interface_status():
    return jsonify({
        "interface_core": "online",
        "message": "Interface styling API is active"
    }), 200

# 🔌 Plugin spec for external module injection
@interface_api.route("/plugin/spec", methods=["GET"])
def plugin_spec():
    return jsonify({
        "plugin_support": True,
        "method": "Blueprint injection",
        "path_format": "branches/{plugin_name}/routes.py",
        "requirements": {
            "register_function": "Blueprint() instance",
            "endpoint_prefix": "/api/{plugin_name}"
        },
        "example": {
            "name": "sentiment_plugin",
            "path": "branches/sentiment_plugin/routes.py",
            "prefix": "/api/sentiment"
        }
    }), 200

# 🖥️ Live interface map of renderable components
@interface_api.route("/style/live", methods=["GET"])
def live_interface():
    return jsonify({
        "ui_status": "interactive",
        "components": [
            "persona_panel",
            "chat_stream",
            "memory_snapshot",
            "reflex_feedback"
        ],
        "stream_endpoint": "/api/chat/stream",
        "design_mode": "adaptive"
    }), 200

# 📊 Real-time interface status + visual readiness
@interface_api.route("/style/status", methods=["GET"])
def interface_readiness():
    return jsonify({
        "interface": {
            "theme": "dark",
            "mode": "reflective",
            "stream": True,
            "plugin_support": True,
            "active_panels": 4
        },
        "status": "ready",
        "timestamp": int(time.time())
    }), 200
