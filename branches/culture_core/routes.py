from flask import Blueprint, request, jsonify

culture_bp = Blueprint("culture_bp", __name__)

@culture_bp.route("/context", methods=["POST"])
def cultural_context():
    region = request.json.get("region", "global")
    language = request.json.get("language", "en")
    norms = {
        "global": "neutral tone, inclusive phrasing",
        "jp": "respect hierarchy, indirect framing",
        "us": "direct tone, casual familiarity"
    }

    return jsonify({
        "region": region,
        "language": language,
        "localization": norms.get(region, "neutral defaults applied"),
        "status": "localized context embedded"
    })
