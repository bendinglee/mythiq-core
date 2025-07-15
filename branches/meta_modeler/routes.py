from flask import Blueprint, request, jsonify
from .persona_exporter import export_persona
from .conversation_sampler import sample_for_training
from .model_builder import build_schema

meta_api = Blueprint("meta_api", __name__)

@meta_api.route("/api/meta/model", methods=["POST"])
def build_model():
    turns = request.json.get("turns", [])
    persona = export_persona()
    samples = sample_for_training(turns)
    schema = build_schema(persona, samples)
    return jsonify(schema)
