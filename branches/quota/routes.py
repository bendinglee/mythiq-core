from flask import Blueprint, request, jsonify
from .store import update_quota

quota_bp = Blueprint("quota_bp", __name__)

@quota_bp.route("/api/quota", methods=["POST"])
def track_usage():
    data = request.json or {}
    user_id = data.get("user_id")
    quota = update_quota(user_id)
    return jsonify({"usage": quota["count"], "status": "tracked"})
