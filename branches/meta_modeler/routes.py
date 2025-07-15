from flask import Blueprint, jsonify
import time, os
from subprocess import check_output

meta_api = Blueprint("meta_api", __name__)

def get_commit_hash():
    try:
        return check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except:
        return "unknown"

@meta_api.route("/snapshot", methods=["GET"])
def snapshot():
    return jsonify({
        "system": "Mythiq",
        "boot_timestamp": time.time(),
        "git_commit": get_commit_hash(),
        "runtime": f"Python {os.sys.version_info.major}.{os.sys.version_info.minor}",
        "modules": sorted(os.listdir("branches"))
    }), 200
