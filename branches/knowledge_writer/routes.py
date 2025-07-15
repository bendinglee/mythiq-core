from flask import Blueprint, request, jsonify
from .style_controller import apply_style
from .memory_injector import inject_memory
from .revision_tool import revise_text

writer_bp = Blueprint("writer_bp", __name__)

@writer_bp.route("/draft", methods=["POST"])
def draft():
    prompt = request.json.get("topic", "")
    context = inject_memory(prompt)
    styled = apply_style(context)
    return jsonify({ "draft": styled })

@writer_bp.route("/finalize", methods=["POST"])
def finalize():
    draft = request.json.get("draft", "")
    revised = revise_text(draft)
    return jsonify({ "final": revised })
