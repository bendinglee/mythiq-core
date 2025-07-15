from flask import Blueprint, request, jsonify
from .prompt_sculptor import sculpt_prompt
from .dream_synth import synthesize_dream
from .lucid_editor import edit_dream

dream_bp = Blueprint("dream_bp", __name__)

@dream_bp.route("/api/dream", methods=["POST"])
def dream_engine():
    base = request.json.get("prompt", "")
    sculpted = sculpt_prompt(base)
    dream = synthesize_dream(sculpted)
    tweak = request.json.get("edit", "")
    if tweak:
        dream = edit_dream(dream, tweak)
    return jsonify(dream)
