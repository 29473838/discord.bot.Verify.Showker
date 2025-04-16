from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import View, Button
import os

auth_role_name = None
auth_channel_id = None

def setup_commands(bot):
    @bot.command(name="인증")
    async def send_auth(ctx):
        if auth_channel_id is None:
            await ctx.send("먼저 !인증 채널 (채널명) 을 입력해주세요.")
            return

        embed = Embed(title="사용자 인증", description="아래 버튼을 눌러 인증을 시작하세요.")
        button = Button(label="인증하기", style=ButtonStyle.link, url=os.getenv("AUTH_WEB_URL") + "/consent")
        view = View()
        view.add_item(button)

        channel = bot.get_channel(auth_channel_id)
        await channel.send(embed=embed, view=view)

    @bot.command(name="인증")
    async def 인증(ctx):
        await ctx.send("!인증 채널 (채널명), !인증 역할 (역할명)을 먼저 설정해주세요.")

    @bot.command(name="인증채널")
    async def set_channel(ctx, channel_name: str):
        global auth_channel_id
        for ch in ctx.guild.text_channels:
            if ch.name == channel_name:
                auth_channel_id = ch.id
                await ctx.send(f"인증 채널 설정 완료: {channel_name}")
                return
        await ctx.send("채널을 찾을 수 없습니다.")

    @bot.command(name="인증역할")
    async def set_role(ctx, role_name: str):
        global auth_role_name
        auth_role_name = role_name
        await ctx.send(f"인증 역할 설정 완료: {role_name}")
