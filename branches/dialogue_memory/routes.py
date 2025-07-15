from flask import Blueprint, jsonify

dialogue_memory_api = Blueprint("dialogue_memory_api", __name__)

@dialogue_memory_api.route("/pulse", methods=["GET"])
def dialogue_memory_status():
    return jsonify({
        "dialogue_memory": "online",
        "message": "Dialogue memory node listening"
    })
