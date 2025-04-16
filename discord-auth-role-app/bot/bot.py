import discord
from discord.ext import commands
from commands import setup_commands
import os

intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠 권한 활성화
intents.members = True  # 맴버 권한 활성화
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"봇 로그인됨: {bot.user}")
    setup_commands(bot)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
