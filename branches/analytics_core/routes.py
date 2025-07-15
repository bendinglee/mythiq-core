from flask import Blueprint, jsonify, request
from .trend_monitor import get_trend

# 📈 Analytics blueprint setup
analytics_bp = Blueprint("analytics_bp", __name__)

# 🔍 GET /trend — return high-level trend report
@analytics_bp.route("/trend", methods=["GET"])
def trend_report():
    return jsonify(get_trend())

# 🧪 POST /trend/test — register mock analytics payload
@analytics_bp.route("/trend/test", methods=["POST"])
def log_dummy_event():
    data = request.get_json(silent=True)
    return jsonify({
        "status": "received",
        "payload": data,
        "message": "Dummy analytics event registered"
    }), 200

# 📊 GET /metrics — system snapshot of performance and triggers
@analytics_bp.route("/metrics", methods=["GET"])
def system_metrics():
    return jsonify({
        "uptime": "47 minutes",
        "requests": 215,
        "avg_latency": "122ms",
        "trigger_rate": {
            "persona_reflect": 32,
            "goal_update": 19,
            "reload": 4
        }
    }), 200
