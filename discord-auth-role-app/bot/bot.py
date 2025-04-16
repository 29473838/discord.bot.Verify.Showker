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

@bot.command(name="인증")
async def send_auth(ctx):
    await ctx.send("인증 명령 실행!")

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
