from flask import Blueprint, jsonify
import time

status_bp = Blueprint("status_bp", __name__)

@status_bp.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "timestamp": time.time()
    }), 200
