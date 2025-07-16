from flask import Blueprint, jsonify
import time

echo_bp = Blueprint("echo_bp", __name__)

@echo_bp.route("/echo", methods=["GET"])
def echo_memory():
    timeline = [
        {"event": "reflex_surge", "emotion": "curious", "time": int(time.time()) - 3600},
        {"event": "goal_convergence", "emotion": "focused", "time": int(time.time())}
    ]
    return jsonify({
        "timeline": timeline,
        "status": "memory echo retrieved"
    })
