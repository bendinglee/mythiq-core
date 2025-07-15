from flask import Blueprint, request, jsonify
from .prompt_formatter import format_prompt
from .diffusion_engine import generate_image

image_bp = Blueprint("image_bp", __name__)

@image_bp.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    persona = data.get("persona", {})
    
    formatted_prompt = format_prompt(prompt, persona)
    image_url = generate_image(formatted_prompt)
    
    return jsonify({
        "prompt": formatted_prompt,
        "image_url": image_url
    })
