from flask import Blueprint, request, jsonify

symbol_bp = Blueprint("symbol_bp", __name__)

@symbol_bp.route("/synthesize", methods=["POST"])
def synthesize():
    tags = request.json.get("tags", [])
    glyphs = [f"⚙️ {tag}" if "core" in tag else f"✨ {tag}" for tag in tags]

    return jsonify({
        "symbols": glyphs,
        "source_tags": tags,
        "status": "symbolic cognition rendered"
    })
