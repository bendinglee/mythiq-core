from flask import Blueprint, request, jsonify

install_bp = Blueprint("install_bp", __name__)

@install_bp.route("/install", methods=["POST"])
def install_plugin():
    plugin_name = request.json.get("name", "undefined")
    path = f"branches/{plugin_name}/routes.py"

    return jsonify({
        "plugin": plugin_name,
        "path": path,
        "method": "Blueprint injection",
        "status": "installation route created"
    })
