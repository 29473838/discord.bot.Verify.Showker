import gspread
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from gspread_formatting import format_cell_range, cellFormat, textFormat, colors

# 환경변수 불러오기
load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, '..', 'credentials.json')

SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "인증리스트")  # 기본값 지정
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Google Sheets 인증
def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    return client

# 스프레드시트 열기
def open_spreadsheet():
    try:
        client = authenticate_google_sheets()
        sheet = client.open(SPREADSHEET_NAME).sheet1
        return sheet
    except Exception as e:
        print(f"[ERROR] 스프레드시트를 열 수 없습니다: {e}")
        return None

# 스타일 적용 (헤더 스타일 등)
def apply_styles(sheet):
    try:
        # A1 셀: 회색 배경 + 흰 글씨 + 볼드
        format_cell_range(sheet, 'A1', cellFormat(
            backgroundColor=colors.Color(0.5, 0.5, 0.5),
            textFormat=textFormat(bold=True, foregroundColor=colors.Color(1, 1, 1))
        ))

        # B1:D1 셀: 초록색 배경 + 흰 글씨 + 볼드
        format_cell_range(sheet, 'B1:D1', cellFormat(
            backgroundColor=colors.Color(0, 0.5, 0),
            textFormat=textFormat(bold=True, foregroundColor=colors.Color(1, 1, 1))
        ))

        # A2 셀: 가운데 정렬
        format_cell_range(sheet, 'A2', cellFormat(
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE'
        ))
    except Exception as e:
        print(f"[ERROR] 셀 스타일 적용 중 오류 발생: {e}")

# 전체 적용 함수
def update_spreadsheet():
    sheet = open_spreadsheet()
    if sheet:
        apply_styles(sheet)
