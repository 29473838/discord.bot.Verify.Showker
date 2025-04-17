import json
import os
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 상수 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = 'Sheet1'
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 구글 시트 인증 함수
def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(credentials)

# 구글 시트에 유저 정보 저장
def save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region):
    client = authenticate_google_sheets()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    row = [discord_id, username, joined_at, ip, country, region]
    sheet.append_row(row)

# 유저 정보 저장 (로컬 + 구글 시트)
def save_user_info(discord_id, username, joined_at, ip, country, region):
    try:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append({
        "discord_id": discord_id,
        "username": username,
        "joined_at": joined_at,
        "ip": ip,
        "country": country,
        "region": region
    })

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region)

# 로컬 JSON에서 유저 목록 불러오기
def get_users():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# 구글 시트 객체 반환
def get_google_sheet():
    client = authenticate_google_sheets()
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
