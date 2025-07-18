from flask import Blueprint, jsonify

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/test", methods=["GET"])
def test_auth():
    return jsonify({
        "status": "ok",
        "module": "auth_gate",
        "message": "Auth route is working!"
    })
