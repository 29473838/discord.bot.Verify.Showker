# generate_env_json.py
import json

with open("credentials.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)

json_str = json.dumps(credentials).replace("\n", "\\n")
print(json_str)
