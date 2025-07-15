from flask import Blueprint, request, jsonify
from .feedback_collector import update_score
from .style_evolver import evolve_style

tune_bp = Blueprint("tune_bp", __name__)

@tune_bp.route("/score/update", methods=["POST"])
def feedback():
    score = update_score(request.json)
    return jsonify(score)

@tune_bp.route("/persona/evolve", methods=["POST"])
def evolve():
    update = evolve_style(request.json)
    return jsonify(update)
