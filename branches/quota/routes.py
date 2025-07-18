from flask import Blueprint, jsonify

quota_bp = Blueprint("quota_bp", __name__)

@quota_bp.route("/test", methods=["GET"])
def test_quota():
    return jsonify({
        "status": "ok",
        "module": "quota",
        "message": "Quota module is alive!"
    })
