# generate_env_json.py
import json

with open("credentials.json", "r", encoding="utf-8") as f:
    creds = json.load(f)

# private_key 줄바꿈을 이스케이프하여 env용 문자열로 변환
creds["private_key"] = creds["private_key"].replace("\n", "\\n")
print(json.dumps(creds))