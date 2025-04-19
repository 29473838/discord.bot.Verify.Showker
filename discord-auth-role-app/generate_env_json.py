# generate_env_json.py
import json

with open("credentials.json", "r") as f:
    creds = json.load(f)
    env_str = json.dumps(creds).replace("\n", "\\n")
    print(env_str)