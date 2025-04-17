import gspread
from google.oauth2 import service_account
from gspread_formatting import *
from gspread_formatting import colors
import os

# 인증 함수
def authenticate_google_sheets():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(BASE_DIR, '..', 'credentials.json')  # 실제 경로로 수정하세요

    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)
    return client

# 스프레드시트 열기 함수
def open_spreadsheet():
    client = authenticate_google_sheets()
    sheet = client.open('인증리스트').sheet1  # 실제 스프레드시트 이름으로 수정
    return sheet

# 스타일 적용 함수
def update_spreadsheet():
    sheet = open_spreadsheet()

    # 셀 스타일 적용: A1 셀 배경색, 글꼴 색상 변경
    format_cell_range(sheet, 'A1', cellFormat(
        backgroundColor=colors.Color(0.5, 0.5, 0.5),
        textFormat=textFormat(bold=True, foregroundColor=colors.Color(1, 1, 1))
    ))

    # 여러 셀에 스타일 적용
    format_cell_range(sheet, 'B1:D1', cellFormat(
        backgroundColor=colors.Color(0, 0.5, 0),
        textFormat=textFormat(bold=True, foregroundColor=colors.Color(1, 1, 1))
    ))

    # 텍스트 정렬: A2 셀 텍스트 가운데 정렬
    format_cell_range(sheet, 'A2', cellFormat(
        horizontalAlignment='CENTER',
        verticalAlignment='MIDDLE'
    ))
