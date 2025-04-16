from flask import Flask, render_template, request, redirect, url_for
from shared.database import save_user_info, get_users
import socket
import requests
import sys
import os
import asyncio
import discord
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.database import save_user_info, get_users

app = Flask(__name__)

# Discord 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route("/consent")
def consent():
    return render_template("consent.html")

@app.route("/submit", methods=["POST"])
def submit():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    discord_id = request.form.get("discord_id")
    username = request.form.get("username")
    joined_at = request.form.get("joined_at")

    # 국가 및 위치 조회
    geo = requests.get(f"http://ip-api.com/json/{ip}").json()
    country = geo.get("country")
    region = geo.get("regionName")

    save_user_info(discord_id, username, joined_at, ip, country, region)
    return render_template("success.html")

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
    if code:
        # 여기서 'code'로 액세스 토큰을 얻는 로직 추가
        return f"Authorization code: {code}"
    return "No code received."

@bot.event
async def on_ready():
    print(f"봇 로그인됨: {bot.user}")

@bot.command(name="인증")
async def send_auth(ctx):
    await ctx.send("인증 명령 실행!")

# Flask 서버와 Discord 봇을 동시에 실행
def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(os.getenv('DISCORD_BOT_TOKEN')))
    loop.run_forever()

if __name__ == '__main__':
    from threading import Thread
    thread = Thread(target=run_bot)
    thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)