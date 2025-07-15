from flask import Blueprint, jsonify

ethics_api = Blueprint("ethics_api", __name__)

@ethics_api.route("/ping", methods=["GET"])
def ethics_status():
    return jsonify({
        "ethics_engine": "online",
        "message": "Ethics core active and evaluative"
    })
