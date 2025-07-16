from flask import Blueprint, request, jsonify
import time

visualstory_bp = Blueprint("visualstory_bp", __name__)

# 🎞️ /narrative/image/gen — Generate story visuals from anchors
@visualstory_bp.route("/image/gen", methods=["POST"])
def generate_visual_story():
    inputs = request.json.get("anchors", [])
    frames = [{"id": i+1, "label": a.get("label", "scene"), "visual": f"🖼 Frame of {a.get('label', 'scene')}"} for i, a in enumerate(inputs)]

    return jsonify({
        "storyboard": frames,
        "timestamp": int(time.time()),
        "status": "visual story rendered"
    })

# 🎭 /narrative/persona/render — Render visual persona + tone fusion
@visualstory_bp.route("/persona/render", methods=["POST"])
def render_persona_visual():
    persona = request.json.get("persona", {})
    tone = persona.get("tone", "neutral")
    name = persona.get("name", "Mythiq")
    goal = persona.get("goal", "expressive cognition")

    render = f"{name} glows in a '{tone}' tone, striving to {goal}"

    return jsonify({
        "rendered_persona": render,
        "status": "persona visual rendered"
    })
