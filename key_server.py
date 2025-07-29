from datetime import datetime
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-key", methods=["GET", "POST"])
def get_key():
    if request.method == "POST":
        data = request.get_json()
        group = data.get("group")
        filename = data.get("filename")
    elif request.method == "GET":
        group = request.args.get("group")
        filename = request.args.get("filename")
    else:
        return "Invalid method", 405

    log_entry = f"[{datetime.now()}] {request.method} /get-key | group={group}, filename={filename} | "

    if not group or not filename:
        log_entry += "Denied (missing group or filename)\n"
        _log_request(log_entry)
        return "Missing group or filename", 400

    # Load access policy
    if not os.path.exists("policy.json"):
        log_entry += "Denied (no policy file)\n"
        _log_request(log_entry)
        return "Access policy not found", 400

    import json
    with open("policy.json", "r") as f:
        policy = json.load(f)

    allowed_groups = policy.get(filename)
    if not allowed_groups or group not in allowed_groups:
        log_entry += "Denied (group not allowed)\n"
        _log_request(log_entry)
        return "Access denied", 400

    key_path = filename + ".key"
    if not os.path.exists(key_path):
        log_entry += "Denied (key file not found)\n"
        _log_request(log_entry)
        return "Key not found", 404

    with open(key_path, "rb") as f:
        key = f.read()

    log_entry += "Granted\n"
    _log_request(log_entry)
    return jsonify({"key": key.decode()})


def _log_request(entry):
    with open("key_log.txt", "a") as f:
        f.write(entry)

if __name__ == "__main__":
    app.run(port=5050)
