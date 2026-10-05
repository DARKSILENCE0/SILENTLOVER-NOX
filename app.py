from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


def detect_target(target):
    target = target.strip()

    if not target:
        return "unknown"

    # Email
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", target):
        return "email"

    # IPv4
    if re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", target):
        return "ip"

    # Domain
    if re.match(
        r"^(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$",
        target
    ):
        return "domain"

    # Username / other target
    return "username"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    target = data.get("target", "").strip()

    if not target:
        return jsonify({
            "success": False,
            "error": "Target is required."
        }), 400

    target_type = detect_target(target)

    results = []

    results.append({
        "module": "Target Detection",
        "status": "success",
        "data": f"Detected target type: {target_type}"
    })

    results.append({
        "module": "OSINT Engine",
        "status": "ready",
        "data": "Public-source intelligence modules are ready."
    })

    return jsonify({
        "success": True,
        "target": target,
        "type": target_type,
        "results": results
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "online",
        "name": "SILENTLOVER NOX"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
