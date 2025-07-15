from flask import Blueprint, request, jsonify
from .vault_keeper import store_data
from .unlock_logic import unlock_data

secure_bp = Blueprint("secure_bp", __name__)

@secure_bp.route("/store", methods=["POST"])
def store():
    return jsonify(store_data(request.json))

@secure_bp.route("/unlock", methods=["POST"])
def unlock():
    token = request.json.get("token", "")
    return jsonify(unlock_data(token))
