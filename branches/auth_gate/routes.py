from flask import Blueprint, jsonify
import time

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/test", methods=["GET"])
def test_auth():
    return jsonify({
        "status": "success",
        "module": "auth_gate",
        "message": "Auth gateway is active.",
        "timestamp": time.time()
    }), 200
