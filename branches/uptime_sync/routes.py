from flask import Blueprint, jsonify
import time

network_bp = Blueprint("network_bp", __name__)

@network_bp.route("/network", methods=["GET"])
def network_status():
    return jsonify({
        "mesh_status": "online",
        "agents": 12,
        "timestamp": int(time.time()),
        "status": "network check complete"
    })
