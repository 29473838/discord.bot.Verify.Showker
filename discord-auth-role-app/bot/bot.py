import discord
from discord.ext import commands
import commands as bot_commands  # commands.py를 불러옴
import os
from dotenv import load_dotenv

# 환경 변수 로드 (.env 파일 사용 시)
load_dotenv()

# 인증 설정 (임시 변수 - 휘발성)
auth_channel_id = None
auth_role_name = None

# 인텐트 설정 (명령어 인식 필수)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True


# 봇 인스턴스 생성 (commands.py에서 생성된 봇 사용)
bot = bot_commands.bot


# 봇 인텐트 설정
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

# 봇 인스턴스 생성 (commands.py에서 생성된 봇 사용)
bot = bot_commands.bot

# 봇이 준비되었을 때 한 번만 불러오는 이벤트
@bot.event
async def on_ready():
    # 슬래시 커맨드를 디스코드에 동기화합니다.
    await bot.tree.sync()
    print(f"✅ 봇 로그인됨: {bot.user} (슬래시 커맨드 동기화 완료)")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    else:
        bot.run(TOKEN)