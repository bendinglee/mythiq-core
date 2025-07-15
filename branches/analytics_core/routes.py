from flask import Blueprint, jsonify, request
from .trend_monitor import get_trend

analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.route("/trend", methods=["GET"])
def trend_report():
    return jsonify(get_trend())

@analytics_bp.route("/trend/test", methods=["POST"])
def log_dummy_event():
    data = request.get_json(silent=True)
    return jsonify({
        "status": "received",
        "payload": data,
        "message": "Dummy analytics event registered"
    }), 200
