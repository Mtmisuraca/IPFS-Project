import os
import json
import base64
import subprocess
from cryptography.fernet import Fernet
import requests
import shlex
from datetime import datetime

# Load session
if os.path.exists("session.json"):
    with open("session.json", "r") as f:
        session = json.load(f)
        username = session["username"]
        group = session["group"]
        print(f"Session loaded: {username} in group {group}")
else:
    print("No active session. Please login first.")
    exit()

filename = input("Enter file path to encrypt and upload: ")

# Request key from key server
try:
    print("Requesting encryption key...")
    print(f"Sending to key server: group={group}, filename={filename}")
    res = requests.get("http://localhost:5050/get-key", params={
        "group": group,
        "filename": filename
    })
    if res.status_code != 200:
        print("Key server denied access or failed.")
        exit()
    key = res.json()["key"]
    print("Received key:", key)
except Exception as e:
    print("Failed to contact key server:", e)
    exit()

fernet = Fernet(key)

# Encrypt file
print("Encrypting file...")
with open(filename, "rb") as f:
    data = f.read()
enc_data = fernet.encrypt(data)

# Save encrypted file
enc_filename = filename + ".enc"
with open(enc_filename, "wb") as f:
    f.write(enc_data)

# Save key locally
with open(filename + ".key", "wb") as f:
    f.write(key.encode() if isinstance(key, str) else key)

print("Saved .enc file, requesting IPFS add...")

# Upload to IPFS (fallback method)
try:
    print("Uploading to IPFS using fallback method...")
    process = subprocess.Popen(shlex.split(f'ipfs add "{enc_filename}"'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(timeout=10)

    if process.returncode != 0:
        print("IPFS error:", stderr)
        exit()

    # Extract IPFS hash from output
    ipfs_hash = None
    for line in stdout.strip().splitlines():
        if line.startswith("added ") or line.strip().startswith("Qm"):
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1].startswith("Qm"):
                ipfs_hash = parts[1]
                break

    if not ipfs_hash:
        print("Failed to retrieve IPFS hash.")
        print("IPFS output was:\n", stdout)
        exit()

    print("Uploaded and encrypted: IPFS hash =", ipfs_hash)

except subprocess.TimeoutExpired:
    print("Timeout: IPFS did not respond.")
    exit()
except Exception as e:
    print("IPFS upload failed:", e)
    exit()

# Audit log
timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
with open("audit_log.txt", "a") as f:
    f.write(f"{timestamp} {username} (group: {group}) uploaded {filename} (hash: {ipfs_hash})\n")

# Update policy.json
if os.path.exists("policy.json"):
    with open("policy.json", "r") as f:
        policy = json.load(f)
else:
    policy = {}

policy[filename] = [group]
with open("policy.json", "w") as f:
    json.dump(policy, f, indent=2)
