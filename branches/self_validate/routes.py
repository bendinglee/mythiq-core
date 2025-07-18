from flask import Blueprint, jsonify

validation_bp = Blueprint("validation_bp", __name__)

@validation_bp.route("/test", methods=["GET"])
def test_validation():
    return jsonify({
        "status": "ok",
        "module": "self_validate",
        "message": "Self-validation is active!"
    })
