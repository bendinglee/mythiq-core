from flask import Blueprint, jsonify

bio_bp = Blueprint("bio_bp", __name__)

@bio_bp.route("/ping", methods=["GET"])
def bio_status():
    return jsonify({
        "bio_emotion": "online",
        "message": "Biometric emotion module listening"
    })
