from flask import Blueprint, request, jsonify
import time

sync_bp = Blueprint("sync_bp", __name__)

@sync_bp.route("/sync", methods=["POST"])
def sync_agents():
    agent_ids = request.json.get("agents", [])
    modules = request.json.get("modules", [])

    return jsonify({
        "agents": agent_ids,
        "modules_synced": modules,
        "timestamp": int(time.time()),
        "status": "sync complete"
    })
