from flask import Blueprint, jsonify
import time

quota_bp = Blueprint("quota_bp", __name__)

@quota_bp.route("/test", methods=["GET"])
def test_quota():
    return jsonify({
        "status": "success",
        "module": "quota",
        "message": "Quota module responsive.",
        "timestamp": time.time()
    }), 200
