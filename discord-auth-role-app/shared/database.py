import json
import os

# 절대 경로 기준으로 DATA_FILE 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")


def save_user_info(discord_id, username, joined_at, ip, country, region):
    # 파일이 없으면 빈 리스트로 초기화
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # 기존 데이터 로드 (JSON 깨짐 방지 처리)
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    # 새 정보 추가
    data.append({
        "discord_id": discord_id,
        "username": username,
        "joined_at": joined_at,
        "ip": ip,
        "country": country,
        "region": region
    })

    # 파일에 저장
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_users():
    # 파일이 없으면 빈 리스트 반환
    if not os.path.exists(DATA_FILE):
        return []

    # 데이터 읽기 (깨진 JSON 방지 처리)
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

