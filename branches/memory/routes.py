from flask import Blueprint, jsonify

memory_bp = Blueprint("memory_bp", __name__)

@memory_bp.route("/test", methods=["GET"])
def test_memory():
    return jsonify({
        "status": "ok",
        "module": "memory",
        "message": "Memory service is online!"
    })
