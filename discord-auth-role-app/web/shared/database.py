import json
import os
import gspread
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), '..', os.getenv("SERVICE_ACCOUNT_FILE"))
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = 'Sheet1'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return gspread.authorize(credentials)

def save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region):
    client = authenticate_google_sheets()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    row = [discord_id, username, joined_at, ip, country, region]
    sheet.append_row(row)

def save_user_info(discord_id, username, joined_at, ip, country, region):
    # 로컬에도 저장
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

    # 구글 시트에도 저장
    save_user_info_to_sheets(discord_id, username, joined_at, ip, country, region)

def get_users():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_google_sheet():
    client = authenticate_google_sheets()
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
