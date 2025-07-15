from flask import Blueprint, jsonify

routine_bp = Blueprint("routine_bp", __name__)

@routine_bp.route("/status", methods=["GET"])
def routine_status():
    return jsonify({
        "routine_designer": "online",
        "message": "Routine designer module operational"
    })
