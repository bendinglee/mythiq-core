from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq core is awake",
        "timestamp": __import__('time').time()
    })
