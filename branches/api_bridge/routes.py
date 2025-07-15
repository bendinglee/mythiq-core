from flask import Blueprint, request, jsonify
from .call_handler import fetch_data

bridge_bp = Blueprint("bridge_bp", __name__)

@bridge_bp.route("/fetch", methods=["POST"])
def fetch():
    config = request.json
    return jsonify(fetch_data(config))
