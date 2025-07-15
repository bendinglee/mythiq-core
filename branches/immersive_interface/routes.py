from flask import Blueprint, jsonify

imm_bp = Blueprint("imm_bp", __name__)

@imm_bp.route("/ping", methods=["GET"])
def immersive_status():
    return jsonify({
        "immersive_interface": "online",
        "message": "Immersive experience engine engaged"
    })
