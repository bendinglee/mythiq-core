from flask import Blueprint, jsonify

docs_bp_ui = Blueprint("docs_bp_ui", __name__)

@docs_bp.route("/docs/swagger", methods=["GET"])
def swagger_ui():
    return jsonify({
        "ui": "Swagger viewer endpoint",
        "link": "/api/swagger.json",
        "status": "UI ready"
    })
