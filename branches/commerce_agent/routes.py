from flask import Blueprint, jsonify

commerce_bp = Blueprint("commerce_bp", __name__)

@commerce_bp.route("/health", methods=["GET"])
def commerce_status():
    return jsonify({
        "commerce_agent": "online",
        "message": "Commerce agent is ready for transactions"
    })
