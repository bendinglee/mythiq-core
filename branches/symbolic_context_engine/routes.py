from flask import Blueprint, request, jsonify

symbol_bp = Blueprint("symbol_bp", __name__)

# 🔣 /symbol/map/context — Map memory anchors to symbolic representation
@symbol_bp.route("/map/context", methods=["POST"])
def map_context_symbols():
    anchors = request.json.get("anchors", [])
    mapped = [{"anchor": a.get("label", "unknown"), "symbol": f"⚡{a.get('label','')[:2].upper()}"} for a in anchors]

    return jsonify({
        "symbol_map": mapped,
        "status": "symbols generated from context"
    })

# 🧠 /symbol/analogy/build — Build analogies from abstract context
@symbol_bp.route("/analogy/build", methods=["POST"])
def build_analogy():
    source = request.json.get("source", "memory")
    target = request.json.get("target", "emotion")

    analogy = f"{source} is to {target} as spark is to fire."

    return jsonify({
        "source": source,
        "target": target,
        "analogy": analogy,
        "status": "analogy synthesized"
    })
