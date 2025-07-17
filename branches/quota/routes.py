from flask import Blueprint, request, jsonify
from .store import load_quota, update_quota

quota_bp = Blueprint("quota_bp", __name__)
MAX_FREE_QUOTA = 100

@quota_bp.route("/api/quota", methods=["POST"])
def record_usage():
    data = request.json or {}
    user_id = data.get("user_id")

    usage = update_quota(user_id)
    capped = usage["count"] >= MAX_FREE_QUOTA

    return jsonify({
        "user_id": user_id,
        "count": usage["count"],
        "limit_exceeded": capped
    })
