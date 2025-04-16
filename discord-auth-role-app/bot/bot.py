import discord
from discord.ext import commands
from commands import setup_commands
import os

# Discord 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ 봇 로그인됨: {bot.user}")
    setup_commands(bot)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
