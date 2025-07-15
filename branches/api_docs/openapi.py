from flask import Blueprint, jsonify

swagger_bp = Blueprint("swagger_bp", __name__)

@swagger_bp.route("/openapi.json", methods=["GET"])
def openapi_json():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Mythiq API",
            "version": "1.0.0"
        },
        "paths": {
            "/api/meta/model/snapshot": { "get": { "summary": "System identity" }},
            "/api/memory/explore/summary": { "get": { "summary": "Session anchor reflection" }},
            "/api/docs": { "get": { "summary": "Route map overview" }}
        }
    })
