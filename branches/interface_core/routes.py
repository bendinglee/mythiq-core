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
