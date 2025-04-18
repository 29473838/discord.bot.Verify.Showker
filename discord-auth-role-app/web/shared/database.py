from flask import Flask, render_template, request
from shared.database import save_user_info, get_users, get_google_sheet
from shared.spreadsheet import update_spreadsheet
import requests
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "서버가 실행 중입니다."

@app.route("/consent")
def consent():
    return render_template("consent.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")
        discord_id = request.form.get("discord_id")
        username = request.form.get("username")
        joined_at = request.form.get("joined_at")

        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = geo.get("country")
        region = geo.get("regionName")

        save_user_info(discord_id, username, joined_at, ip, country, region)
        update_spreadsheet()  # 구글 시트 업데이트
        return render_template("success.html")
    except Exception as e:
        return f"에러 발생: {str(e)}", 500

@app.route("/admin")
def admin():
    users = get_users()
    return {"users": users}

@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Error: {error}", 400

    code = request.args.get("code")
    if not code:
        return "No code received."

    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
        "scope": "identify guilds.join"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    if resp.status_code != 200:
        return f"Discord 인증 실패: {resp.text}", 500
    return resp.json()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
