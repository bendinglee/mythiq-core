from flask import Blueprint, jsonify
import time

uptime_api = Blueprint("uptime_api", __name__)
START = time.time()

@uptime_api.route("/api/uptime/pulse", methods=["GET"])
def uptime():
    return jsonify({
        "uptime_seconds": round(time.time() - START, 2),
        "boot_timestamp": START
    })
