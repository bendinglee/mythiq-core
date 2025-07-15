from flask import Blueprint, request, jsonify
from .retriever import find_matches
from .answer_builder import build_answer

search_bp = Blueprint("search_bp", __name__)

@search_bp.route("/query", methods=["POST"])
def query():
    q = request.json.get("query", "")
    matches = find_matches(q)
    answer = build_answer(matches)
    return jsonify({ "answer": answer, "matches": matches })

@search_bp.route("/related", methods=["POST"])
def related():
    keyword = request.json.get("keyword", "")
    return jsonify({ "related": find_matches(keyword) })
