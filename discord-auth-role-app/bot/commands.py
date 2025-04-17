import discord
from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import View, Button
import os


# 환경 변수 설정
auth_channel_id = None
auth_role_name = None


# 봇 인텐트 설정
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True 

# 봇 인스턴스 생성
bot = commands.Bot(command_prefix="!", intents=intents)

# 인증 채널 설정 명령어
@bot.command(name="인증채널")
async def set_auth_channel(ctx, channel_name: str):
    global auth_channel_id
    for ch in ctx.guild.text_channels:
        if ch.name == channel_name:
            auth_channel_id = ch.id
            await ctx.send(f"✅ 인증 채널이 `{channel_name}`(으)로 설정되었습니다.")
            return
    await ctx.send("❌ 해당 채널을 찾을 수 없습니다.")

@bot.command()
async def 인증채널(ctx, channel_name: str):
    # 채널 이름이 필요하다는 것을 알려주는 코드
    if not channel_name:
        await ctx.send("채널 이름을 입력해 주세요.")
        return

    # 이후 채널을 사용하는 코드

# 인증 역할 설정 명령어
@bot.command(name="인증역할")
async def set_auth_role(ctx, role_name: str):
    global auth_role_name
    auth_role_name = role_name
    await ctx.send(f"✅ 인증 역할이 `{role_name}`(으)로 설정되었습니다.")

# 인증 메시지를 전송하는 명령어
@bot.command(name="인증메시지")
async def send_auth_message(ctx):
    if auth_channel_id is None:
        await ctx.send("❗ 먼저 `!인증채널 (채널명)`으로 인증 채널을 설정해주세요.")
        return

    embed = Embed(
        title="✅ 디스코드 인증 시스템",
        description="아래 버튼을 눌러 인증을 시작하세요.",
        color=0x00ff00
    )
    auth_url = os.getenv("AUTH_WEB_URL", "http://localhost:5000") + "/consent"
    button = Button(label="인증하기", style=ButtonStyle.link, url=auth_url)
    view = View()
    view.add_item(button)

    channel = bot.get_channel(auth_channel_id)
    if channel:
        await channel.send(embed=embed, view=view)
        await ctx.send("✅ 인증 메시지를 전송했습니다.")
    else:
        await ctx.send("❌ 설정된 인증 채널을 찾을 수 없습니다.")

# 기본 인증 명령어 (가이드 제공)
@bot.command(name="인증")
async def auth_help(ctx):
    await ctx.send("🛠 먼저 `!인증채널 (채널명)` 및 `!인증역할 (역할명)`을 설정한 후 `!인증메시지`를 사용하세요.")

# 봇 준비 완료 이벤트
@bot.event
async def on_ready():
    print(f"✅ 봇이 로그인되었습니다: {bot.user}")

# 봇 실행 (이 부분은 main.py에서 실행하거나 조건부 실행 필요)
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))