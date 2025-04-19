import json
import os
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 상수 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
SERVICE_ACCOUNT_FILE = os.getenv(
    "SERVICE_ACCOUNT_FILE",
    os.path.join(BASE_DIR, "..", "credentials.json")
)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Google Sheets 인증
# GOOGLE_CREDENTIALS_JSON이 설정되어 있으면 이를 사용하고,
# 그렇지 않으면 SERVICE_ACCOUNT_FILE을 사용

def authenticate_google_sheets():
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not credentials_json:
    raise ValueError("❌ GOOGLE_CREDENTIALS_JSON 환경 변수가 비어있습니다.")

    try:
        info = json.loads(credentials_json)
    except json.JSONDecodeError as e:
       raise ValueError(f"❌ GOOGLE_CREDENTIALS_JSON 파싱 오류: {e}")
       
    if credentials_json:
        info = json.loads(credentials_json)
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=SCOPES
        )
    else:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            raise FileNotFoundError(
                f"SERVICE_ACCOUNT_FILE not found: {SERVICE_ACCOUNT_FILE}"
            )
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
    return gspread.authorize(creds)

# 구글 시트에 유저 정보 저장

def save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region):
    client = authenticate_google_sheets()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    row = [discord_id, username, joined_at, ip, country, region]
    sheet.append_row(row)

# 유저 정보 저장 (로컬 + 구글 시트)

def save_user_info(discord_id, username, joined_at, ip, country, region):
    # 로컬 JSON 초기화
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # 기존 데이터 로드
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    # 데이터 추가
    entry = {
        'discord_id': discord_id,
        'username': username,
        'joined_at': joined_at,
        'ip': ip,
        'country': country,
        'region': region
    }
    data.append(entry)

    # 로컬에 저장
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 구글 시트에도 저장
    save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region)

# 로컬 JSON에서 유저 목록 불러오기

def get_users():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# 구글 시트 워크시트 반환

def get_google_sheet():
    client = authenticate_google_sheets()
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
