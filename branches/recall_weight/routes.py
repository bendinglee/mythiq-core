from flask import Blueprint, request, jsonify

weight_bp = Blueprint("weight_bp", __name__)

@weight_bp.route("/weight", methods=["POST"])
def recall_weight():
    anchors = request.json.get("anchors", [])
    scored = [{ "label": a.get("label", "unknown"), "score": len(a.get("label", "")) * 2 } for a in anchors]

    return jsonify({
        "anchors": scored,
        "status": "recall weighting applied"
    })
