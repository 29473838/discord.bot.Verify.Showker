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

# 봇 실행
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN이 설정되지 않았습니다.")
    else:
        bot.run(token)