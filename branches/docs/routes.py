from flask import Blueprint, jsonify

docs_bp = Blueprint("docs_bp", __name__)

@docs_bp.route("/api/docs", methods=["GET"])
def docs_index():
    return jsonify({
        "docs": "Mythiq API Documentation",
        "routes": [
            "/api/brain",
            "/api/ai/query",
            "/api/ai/generate",
            "/api/ai/qa",
            "/api/ai/summarize",
            "/api/intent/route",
            "/api/reason",
            "/api/ai-proxy"
        ],
        "status": "online"
    })
