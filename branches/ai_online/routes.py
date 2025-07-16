from flask import Blueprint, jsonify

online_bp = Blueprint("online_bp", __name__)

@online_bp.route("/online", methods=["GET"])
def online_status():
    return jsonify({
        "ai_state": "awake",
        "mode": "always-on",
        "message": "Mythiq is online and streaming cognition",
        "status": "broadcast active"
    })
