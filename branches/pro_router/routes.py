from flask import Blueprint, jsonify

pro_router_bp = Blueprint("pro_router_bp", __name__)

@pro_router_bp.route("/test", methods=["GET"])
def test_pro_router():
    return jsonify({
        "status": "ok",
        "module": "pro_router",
        "message": "Proxy router is operational!"
    })
