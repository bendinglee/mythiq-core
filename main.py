from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "Minimal Mythiq boot confirmed",
        "timestamp": time.time()
    })

print("✅ Mythiq minimal app is launching...")
app.run(host="0.0.0.0", port=int(__import__('os').getenv("PORT", 5000)))
