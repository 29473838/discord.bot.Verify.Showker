import json
import os

DB_PATH = "shared/user_data.json"

def save_user_info(discord_id, username, joined_at, ip, country, region):
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    data.append({
        "discord_id": discord_id,
        "username": username,
        "joined_at": joined_at,
        "ip": ip,
        "country": country,
        "region": region
    })

    with open(DB_PATH, "w") as f:
        json.dump(data, f)

def get_users():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        return json.load(f)
