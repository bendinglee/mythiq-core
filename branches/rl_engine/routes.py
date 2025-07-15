from flask import Blueprint, jsonify

rl_bp = Blueprint("rl_bp", __name__)

@rl_bp.route("/ping", methods=["GET"])
def rl_status():
    return jsonify({
        "rl_engine": "online",
        "message": "Reinforcement learning module activated"
    })
