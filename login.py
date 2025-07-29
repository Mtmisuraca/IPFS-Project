import json
import getpass

# Load user database
with open("users.json", "r") as f:
    users = json.load(f)

username = input("Username: ").strip()
password = getpass.getpass("Password: ")

# Verify credentials
if username in users and users[username]["password"] == password:
    group = users[username]["group"]
    print(f"Login successful. Group: {group}")

    # Save session
    with open("session.json", "w") as f:
        json.dump({"username": username, "group": group}, f)
else:
    print("Login failed. Invalid username or password.")
