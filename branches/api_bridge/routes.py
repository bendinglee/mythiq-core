from flask import Blueprint, request, jsonify
from .call_handler import fetch_data

bridge_bp_internal = Blueprint("bridge_bp_internal", __name__)

@bridge_bp_internal.route("/fetch", methods=["POST"])
def fetch():
    config = request.json
    return jsonify(fetch_data(config))
