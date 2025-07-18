from flask import Blueprint, jsonify
import time

ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)

@ai_proxy_bp.route("/test", methods=["GET"])
def test_ai_proxy():
    return jsonify({
        "status": "success",
        "module": "ai_proxy",
        "message": "AI Proxy active.",
        "timestamp": time.time()
    }), 200
