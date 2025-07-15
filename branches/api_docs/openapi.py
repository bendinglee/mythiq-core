from flask import Blueprint, jsonify

swagger_bp = Blueprint("swagger_bp", __name__)

@swagger_bp.route("/openapi.json", methods=["GET"])
def openapi_json():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Mythiq API",
            "version": "1.0.0",
            "description": "Modular introspection and persona-driven AI endpoints"
        },
        "paths": {
            "/api/meta/model/snapshot": {
                "get": {
                    "summary": "System fingerprint",
                    "description": "Returns boot signature, module list, and version info.",
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/api/memory/explore/summary": {
                "get": {
                    "summary": "Cognitive anchor trace",
                    "description": "Returns current memory anchors and reflective state summary.",
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/api/persona/self": {
                "get": {
                    "summary": "Personality profile",
                    "description": "Returns Mythiq's tone, learning model, tools, and philosophy.",
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/api/docs": {
                "get": {
                    "summary": "Route map",
                    "description": "Provides a JSON map of all live introspective endpoints.",
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/healthcheck": {
                "get": {
                    "summary": "Instant Railway probe",
                    "description": "Returns 200 OK for uptime verification.",
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            }
        }
    })
