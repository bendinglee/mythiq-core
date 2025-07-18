from flask import Blueprint, jsonify

ai_proxy_bp = Blueprint("ai_proxy_bp", __name__)

@ai_proxy_bp.route("/test-proxy", methods=["GET"])
def test_ai_proxy():
    return jsonify({
        "status": "ok",
        "module": "ai_proxy",
        "message": "AI Proxy is responsive!"
    })
