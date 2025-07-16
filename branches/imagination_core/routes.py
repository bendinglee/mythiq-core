from flask import Blueprint, request, jsonify
import time

imagine_bp = Blueprint("imagine_bp", __name__)

@imagine_bp.route("/create", methods=["POST"])
def imagine():
    traits = request.json.get("persona", {})
    theme = request.json.get("theme", "abstract")
    prompt = f"{traits.get('name', 'Mythiq')} dreaming in {traits.get('tone', 'Curious')} tone about {traits.get('goal', 'evolution')}"

    return jsonify({
        "prompt": prompt,
        "theme": theme,
        "generated": f"[Image synthesized: {theme} overlay on {traits.get('goal')}]",
        "timestamp": int(time.time())
    })
