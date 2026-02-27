from __future__ import annotations

from flask import Flask, jsonify
import yaml
from backup import simulate_get_running_config, save_backup

app = Flask(__name__)


def load_devices() -> list[dict]:
    with open("devices.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("devices", [])


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/devices")
def devices():
    return jsonify(devices=load_devices())


@app.post("/backup")
def run_backup():
    devices = load_devices()
    results = []

    for d in devices:
        cfg = simulate_get_running_config(d)
        path = save_backup(d["name"], cfg)
        results.append({"device": d["name"], "saved_to": path})

    return jsonify(message="Backups created", results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)