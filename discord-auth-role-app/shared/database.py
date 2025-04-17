import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "user_data.json")


def save_user_info(discord_id, username, joined_at, ip, country, region):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    data.append({
        "discord_id": discord_id,
        "username": username,
        "joined_at": joined_at,
        "ip": ip,
        "country": country,
        "region": region
    })

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_users():
    if not os.path.exists(DATA_FILE):
        return []

        
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

    with open(DATA_FILE, 'r') as f:
        return json.load(f)