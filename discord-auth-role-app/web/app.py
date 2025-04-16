from flask import Flask, render_template, request, redirect, url_for
from shared.database import save_user_info, get_users
import socket
import requests
import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.database import save_user_info, get_users

app = Flask(__name__)

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
        return f"Authorization code: {code}"
    return "No code received."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)