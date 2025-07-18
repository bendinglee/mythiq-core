from flask import Blueprint, jsonify
import time

pro_router_bp = Blueprint("pro_router_bp", __name__)

@pro_router_bp.route("/test", methods=["GET"])
def test_pro_router():
    return jsonify({
        "status": "success",
        "module": "pro_router",
        "message": "Pro Router active.",
        "timestamp": time.time()
    }), 200
