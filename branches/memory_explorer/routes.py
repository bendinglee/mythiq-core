from flask import Blueprint, jsonify
from .session_browser import list_sessions
from .route_cluster import group_routes

explorer_bp = Blueprint("explorer_bp", __name__)

@explorer_bp.route("/explore", methods=["GET"])
def explore():
    return jsonify({ "sessions": list_sessions(), "clusters": group_routes() })
