from flask import Blueprint, request, jsonify
from .experiment_builder import build_experiment
from .output_evaluator import evaluate_result

lab_bp = Blueprint("lab_bp", __name__)

@lab_bp.route("/define", methods=["POST"])
def define_exp():
    query = request.json.get("query", "")
    return jsonify(build_experiment(query))

@lab_bp.route("/run", methods=["POST"])
def run_exp():
    result = request.json.get("result", "")
    return jsonify(evaluate_result(result))
