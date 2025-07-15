from flask import Blueprint, jsonify

docs_bp = Blueprint("docs_bp", __name__)

@docs_bp.route("/", methods=["GET"])
def docs_home():
    # Manually map routes or use Flask-RESTX / flask-swag for auto-gen
    return jsonify({
        "/api/meta/model/snapshot": "Returns system signature",
        "/api/memory/explore/summary": "Shows memory anchors",
        "/api/status": "Boot status check",
        "/healthcheck": "Fast Railway check"
    })
