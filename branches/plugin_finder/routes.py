from flask import Blueprint, jsonify

finder_bp = Blueprint("finder_bp", __name__)

@finder_bp.route("/discovery", methods=["GET"])
def discover_plugins():
    plugins = [
        {"name": "sentiment_plugin", "path": "branches/sentiment_plugin/routes.py"},
        {"name": "vision_plugin", "path": "branches/vision_plugin/routes.py"}
    ]
    return jsonify({
        "available_plugins": plugins,
        "status": "discovery complete"
    })
