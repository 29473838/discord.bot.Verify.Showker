import json
import os

# 항상 절대 경로로 파일 경로를 설정 (루트 경로 변화 방지)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")


def save_user_info(discord_id, username, joined_at, ip, country, region):
    # user_data.json 파일이 없으면 초기화
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

    # 기존 데이터 불러오기
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []  # 파일은 있지만 내용이 깨진 경우

    # 새 유저 데이터 추가
    data.append({
        "discord_id": discord_id,
        "username": username,
        "joined_at": joined_at,
        "ip": ip,
        "country": country,
        "region": region
    })

    # 저장
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def get_users():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, 'r') as_
