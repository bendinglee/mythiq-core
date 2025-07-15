from flask import Blueprint, jsonify

story_bp = Blueprint("story_bp", __name__)

@story_bp.route("/heartbeat", methods=["GET"])
def story_status():
    return jsonify({
        "story_maker": "online",
        "message": "Story module booted with empty state"
    })
