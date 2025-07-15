from flask import Blueprint, jsonify
import time, os
from subprocess import check_output

meta_api = Blueprint("meta_api", __name__)

# 🔍 Get current Git commit hash
def get_commit_hash():
    try:
        return check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except Exception:
        return "unknown"

# 🚀 Snapshot system boot and context
@meta_api.route("/snapshot", methods=["GET"])
def snapshot():
    return jsonify({
        "system": "Mythiq",
        "boot_timestamp": time.time(),
        "git_commit": get_commit_hash(),
        "runtime": f"Python {os.sys.version_info.major}.{os.sys.version_info.minor}",
        "modules": sorted(os.listdir("branches"))
    }), 200

# 🧬 Cognitive fingerprint & module profile
@meta_api.route("/fingerprint", methods=["GET"])
def model_fingerprint():
    return jsonify({
        "signature": "mythiq-v1-core",
        "modules": len(os.listdir("branches")),
        "branches_active": [
            "memory_explorer",
            "persona_settings",
            "reflex_core",
            "goal_engine"
        ],
        "learning_gradient": "Reflective + Intent-driven"
    }), 200
