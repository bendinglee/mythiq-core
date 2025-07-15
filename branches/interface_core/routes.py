from flask import Blueprint, jsonify

interface_api = Blueprint("interface_api", __name__)

@interface_api.route("/style/ping", methods=["GET"])
def interface_status():
    return jsonify({
        "interface_core": "online",
        "message": "Interface styling API is active"
    })
