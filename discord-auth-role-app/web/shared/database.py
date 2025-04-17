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

def authenticate_google_sheets():
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not credentials_json:
        raise ValueError("GOOGLE_CREDENTIALS_JSON 환경 변수가 설정되지 않았습니다.")

    info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(
        info,
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
    # JSON 파일이 없거나 비어 있을 경우 초기화
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
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
    # JSON 파일이 없거나 비어 있을 경우 초기화
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# 구글 시트 객체 반환
def get_google_sheet():
    client = authenticate_google_sheets()
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
