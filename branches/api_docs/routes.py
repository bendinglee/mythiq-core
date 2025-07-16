from flask import Blueprint, jsonify

docs_bp = Blueprint("docs_bp", __name__)

@docs_bp.route("/docs", methods=["GET"])
def doc_list():
    return jsonify({
        "docs": [
            {"title": "Core API", "path": "/api/docs"},
            {"title": "Swagger Spec", "path": "/api/swagger.json"}
        ],
        "status": "documentation active"
    })
