from flask import Blueprint, request, jsonify
from .job_queue import launch_task

task_bp = Blueprint("task_bp", __name__)

@task_bp.route("/dispatch", methods=["POST"])
def dispatch_task():
    payload = request.json
    job = launch_task(payload)
    return jsonify({ "job": job })
