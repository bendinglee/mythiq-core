from flask import Blueprint, jsonify
from .media_tracker import get_gallery
import time

gallery_bp = Blueprint("gallery_bp", __name__)

# 🖼 GET /view — return full gallery objects
@gallery_bp.route("/view", methods=["GET"])
def view_gallery():
    return jsonify({ "gallery": get_gallery() })

# 📸 GET /snapshot — cognitive visual snapshot
@gallery_bp.route("/snapshot", methods=["GET"])
def gallery_snapshot():
    return jsonify({
        "snapshot": {
            "title": "Persona Echo",
            "timestamp": int(time.time()),
            "markers": ["memory_explorer", "adaptive_persona", "reflex_core"],
            "status": "rendered"
        }
    })

# 🧾 GET /summary — gallery meta overview
@gallery_bp.route("/summary", methods=["GET"])
def gallery_summary():
    gallery = get_gallery()
    return jsonify({
        "total_items": len(gallery),
        "tags": list({item.get("tag", "untagged") for item in gallery}),
        "latest": gallery[-1] if gallery else {},
        "message": "Gallery metadata summary generated"
    })
