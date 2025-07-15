from flask import Blueprint, jsonify
from .trend_monitor import get_trend

analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.route("/trend", methods=["GET"])
def trend_report():
    return jsonify(get_trend())
