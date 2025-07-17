from flask import Blueprint, request, jsonify
from .store import get_user_memory, save_user_memory

memory_bp = Blueprint("memory_bp", __name__)

@memory_bp.route("/api/memory", methods=["POST"])
def store_memory():
    data = request.json or {}
    user_id = data.get("user_id")
    updates = data.get("updates", {})

    memory = get_user_memory(user_id)
    memory.update(updates)
    save_user_memory(user_id, memory)

    return jsonify({"status": "saved", "memory": memory})

@memory_bp.route("/api/memory", methods=["GET"])
def retrieve_memory():
    user_id = request.args.get("user_id")
    memory = get_user_memory(user_id)
    return jsonify({"memory": memory})
