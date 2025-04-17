from google.oauth2 import service_account
import gspread
from gspread_formatting import *
from gspread_formatting import colors

# gspread 클라이언트 연결
client = gspread.authorize(credentials)

# 구글 스프레드시트 인증 함수
def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/your/service-account-file.json',
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)
    return client

# 스프레드시트 연동
def open_spreadsheet():
    client = authenticate_google_sheets()
    sheet = client.open('Your Spreadsheet Name').sheet1
    return sheet

def update_spreadsheet():
    # 인증 후 스프레드시트 열기
    client = authorize_spreadsheet()
    sheet = client.open('Your Spreadsheet Name').sheet1

    # 셀 스타일 적용: A1 셀 배경색, 글꼴 색상 변경
    cell_range = 'A1'
    format_cell_range(sheet, cell_range, cellFormat(
        backgroundColor=colors.Color(0.5, 0.5, 0.5),  # 회색 배경
        textFormat=textFormat(bold=True, foregroundColor=colors.Color(1, 1, 1))  # 흰색 글씨, 볼드
    ))

    # 여러 셀에 스타일 적용
    cell_range = 'B1:D1'
    format_cell_range(sheet, cell_range, cellFormat(
        backgroundColor=colors.Color(0, 0.5, 0),  # 초록색 배경
        textFormat=textFormat(bold=True, foregroundColor=colors.Color(1, 1, 1))  # 흰색 글씨, 볼드
    ))

    # 텍스트 정렬: A2 셀 텍스트 가운데 정렬
    cell_range = 'A2'
    format_cell_range(sheet, cell_range, cellFormat(
        horizontalAlignment='CENTER',  # 가로 가운데 정렬
        verticalAlignment='MIDDLE'  # 세로 가운데 정렬
    ))
