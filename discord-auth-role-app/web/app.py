from . import init_user_data
from flask import Flask, render_template, request, redirect, url_for
from .shared.database import save_user_info, get_users
import socket
import requests
import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 항상 현재 경로 기준이 아닌 프로젝트 루트 기준으로 경로 지정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "user_data.json")

app = Flask(__name__)

@app.route("/consent")
def consent():
    return render_template("consent.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        discord_id = request.form.get("discord_id")
        username = request.form.get("username")
        joined_at = request.form.get("joined_at")

        print("수신된 값들:", discord_id, username, joined_at)

        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = geo.get("country")
        region = geo.get("regionName")

        save_user_info(discord_id, username, joined_at, ip, country, region)
        return render_template("success.html")
    except Exception as e:
        return f"에러 발생: {str(e)}", 500

@app.route("/admin")
def admin():
    users = get_users()
    return {"users": users}

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return f"Error: {error}", 400

    code = request.args.get('code')
    if not code:
        return "No code received."

    # Discord에 access token 요청
    data = {
        'client_id': os.getenv('DISCORD_CLIENT_ID'),
        'client_secret': os.getenv('DISCORD_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('DISCORD_REDIRECT_URI'),
        'scope': 'identify guilds.join'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    token_json = response.json()

    # 결과 확인
    return token_json

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)