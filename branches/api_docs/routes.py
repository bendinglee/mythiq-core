from flask import Blueprint, jsonify

docs_bp = Blueprint("docs_bp", __name__)

@docs_bp.route("/contribute/map", methods=["GET"])
def contribute_map():
    return jsonify({
        "system": "Mythiq",
        "modules": 42,
        "categories": {
            "Introspection": ["/api/meta/model/snapshot", "/api/persona/self"],
            "Memory": ["/api/memory/explore/summary", "/api/memory/explore/journal"],
            "Identity": ["/api/persona/traits", "/api/meta/model/fingerprint"],
            "Dispatch & Reflex": ["/api/goal", "/api/reflex", "/api/dispatch"],
            "Collaboration": ["/api/contribute/map", "/api/plugin/spec"]
        },
        "plugin_ready": True
    })
