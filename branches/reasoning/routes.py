from flask import Blueprint, jsonify
import time

reasoning_bp = Blueprint("reasoning_bp", __name__)

@reasoning_bp.route("/test", methods=["GET"])
def test_reasoning():
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "message": "Reasoning engine online.",
        "timestamp": time.time()
    }), 200
