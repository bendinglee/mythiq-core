from flask import Blueprint, jsonify
from .metrics_collector import collect_metrics

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/status", methods=["GET"])
def dashboard_status():
    return jsonify(collect_metrics())
