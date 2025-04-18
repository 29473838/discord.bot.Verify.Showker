import os
import json
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# 프로젝트 루트의 credentials.json을 가리키도록
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", os.path.join(BASE_DIR, "credentials.json"))

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 구글 시트 인증 함수
def authenticate_google_sheets():
    # 파일이 실제로 존재하는지 확인
    if not os.path.isfile(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"서비스 계정 키 파일을 찾을 수 없습니다: {SERVICE_ACCOUNT_FILE}")

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(creds)

# 구글 시트에 유저 정보 저장
def save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region):
    client = authenticate_google_sheets()
    sheet = client.open_by_key(os.getenv("SPREADSHEET_ID")).worksheet(os.getenv("SHEET_NAME", "Sheet1"))
    sheet.append_row([discord_id, username, joined_at, ip, country, region])

# ... (기존 로컬 JSON 저장 함수 등은 그대로 두시면 됩니다)
