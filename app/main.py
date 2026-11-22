"""Tiny demo app for the GitOps demo.

Two endpoints:
  GET /         - hello message, shows which environment served the request
  GET /healthz  - liveness/readiness probe endpoint
"""

import os

from flask import Flask, jsonify

app = Flask(__name__)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


@app.route("/")
def hello():
    return jsonify(
        {
            "message": "Hello from the GitOps demo app!",
            "environment": ENVIRONMENT,
        }
    )


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "environment": ENVIRONMENT})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
