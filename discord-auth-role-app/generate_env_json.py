# generate_env_json.py
import json

with open("credentials.json", "r", encoding="utf-8") as f:
    creds = json.load(f)

env_value = json.dumps(creds).replace("\n", "\\n")
print(env_value)
