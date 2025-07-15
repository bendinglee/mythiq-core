from flask import Blueprint, jsonify

context_world_bp = Blueprint("context_world_bp", __name__)

@context_world_bp.route("/ping", methods=["GET"])
def world_context_status():
    return jsonify({
        "world_context": "online",
        "message": "World context node activated"
    })
