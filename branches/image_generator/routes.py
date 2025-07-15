from flask import Blueprint, request, jsonify
from .prompt_formatter import format_prompt
from .diffusion_engine import generate_image

image_bp = Blueprint("image_bp", __name__)

@image_bp.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    persona = data.get("persona", {})  # optional style config

    formatted_prompt = format_prompt(prompt, persona)
    image_result = generate_image(formatted_prompt)

    return jsonify({
        "formatted_prompt": formatted_prompt,
        "result": image_result
    })
