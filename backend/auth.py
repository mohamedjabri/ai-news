import json
import os

USERS_FILE = "users.json"

def load_users():
    """Load user accounts from a JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user accounts to a JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def authenticate(username, password):
    """Check if a username/password is correct."""
    users = load_users()
    return username in users and users[username] == password
