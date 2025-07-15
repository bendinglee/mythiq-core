from flask import Blueprint, jsonify
from .media_tracker import get_gallery

gallery_bp = Blueprint("gallery_bp", __name__)

@gallery_bp.route("/view", methods=["GET"])
def view_gallery():
    return jsonify({ "gallery": get_gallery() })
