from flask import Blueprint, jsonify

reflect_bp = Blueprint("reflect_bp", __name__)

@reflect_bp.route("/pulse", methods=["GET"])
def reflect_status():
    return jsonify({
        "reflector": "online",
        "message": "Self-learning reflection node active"
    })
