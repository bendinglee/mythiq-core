from flask import Blueprint, request, jsonify
from .score_comparator import log_skill_score
from .performance_trends import get_skill_trends

skill_bp = Blueprint("skill_bp", __name__)

@skill_bp.route("/score", methods=["POST"])
def score_skill():
    data = request.json
    return jsonify(log_skill_score(data))

@skill_bp.route("/trends", methods=["GET"])
def trends():
    return jsonify(get_skill_trends())
