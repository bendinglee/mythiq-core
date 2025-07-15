from flask import Blueprint, jsonify

explain_bp = Blueprint("explain_bp", __name__)

@explain_bp.route("/ping", methods=["GET"])
def explain_status():
    return jsonify({
        "explain_core": "online",
        "message": "Explanation engine ready"
    })
