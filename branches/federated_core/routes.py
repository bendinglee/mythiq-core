from flask import Blueprint, jsonify

fed_bp = Blueprint("fed_bp", __name__)

@fed_bp.route("/ping", methods=["GET"])
def federated_status():
    return jsonify({
        "federated_core": "online",
        "message": "Federated logic layer activated"
    })
