from flask import Blueprint, jsonify

swagger_bp = Blueprint("swagger_bp", __name__)

@swagger_bp.route("/swagger.json", methods=["GET"])
def swagger_spec():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Mythiq API",
            "version": "1.0.0"
        },
        "paths": {
            "/api/brain": {"get": {"summary": "Brain orchestrator"}},
            "/api/persona": {"get": {"summary": "Persona fusion engine"}}
        }
    })
