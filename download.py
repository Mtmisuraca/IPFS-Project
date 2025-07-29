import os
import json
import subprocess
from cryptography.fernet import Fernet
import shlex
import requests
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

filename = input("Enter file name to download: ")
ipfs_hash = input("Enter IPFS hash: ")

# Download from IPFS
try:
    print(f"Downloading {ipfs_hash} from IPFS...")
    process = subprocess.Popen(shlex.split(f'ipfs get {ipfs_hash} -o temp_download.enc'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(timeout=10)
    if process.returncode != 0:
        print("IPFS download failed:", stderr)
        exit()
    print("Download complete. Requesting decryption key from key server...")
except Exception as e:
    print("IPFS error:", e)
    exit()

# Request key from key server
try:
    res = requests.get("http://localhost:5050/get-key", params={
        "group": group,
        "filename": filename
    })
    if res.status_code != 200:
        print("Key server denied access or failed.")
        exit()
    key = res.json()["key"]
    print("Received key:", key[:10] + "...")
except Exception as e:
    print("Failed to contact key server:", e)
    exit()

fernet = Fernet(key.encode())

# Decrypt
try:
    with open("temp_download.enc", "rb") as f:
        enc_data = f.read()
    data = fernet.decrypt(enc_data)

    # Save decrypted
    with open(filename + ".decrypted", "wb") as f:
        f.write(data)

    print(f"File downloaded and decrypted as {filename}.decrypted")

    # Log download
    with open("audit_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {username} (group: {group}) downloaded {filename} (hash: {ipfs_hash})\n")

except Exception as e:
    print("Decryption failed:", e)
