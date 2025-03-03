import json
import os

BOOKMARKS_FILE = "bookmarks.json"

def load_bookmarks(user):
    """Load bookmarks for a specific user."""
    if os.path.exists(BOOKMARKS_FILE):
        with open(BOOKMARKS_FILE, "r") as f:
            data = json.load(f)
        return data.get(user, {})
    return {}

def save_bookmarks(user, bookmarks):
    """Save bookmarks for a specific user."""
    if os.path.exists(BOOKMARKS_FILE):
        with open(BOOKMARKS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[user] = bookmarks
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(data, f, indent=4)
