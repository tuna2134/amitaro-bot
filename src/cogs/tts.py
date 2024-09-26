from discord.ext import commands
from discord import app_commands
import discord

from aiohttp import ClientSession

from os import getenv
from io import BytesIO


API_ENDPOINT = getenv("TTS_API_ENDPOINT")


class TTS(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.__session = ClientSession()
        self.connected_channels = []

    async def synthesize(self, ident: str, text: str) -> bytes:
        async with self.__session.post(
            f"{API_ENDPOINT}/synthesize",
            json={"ident": ident, "text": text, "sdp_ratio": 1.4},
        ) as response:
            response.raise_for_status()
            return await response.read()

    @app_commands.command(description="...")
    async def join(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await interaction.followup.send("先に参加してください。")
        else:
            voice_client = await interaction.user.voice.channel.connect()
            self.connected_channels.append(interaction.channel.id)
            await interaction.followup.send("接続しました。")
            voice_client.play(
                discord.FFmpegPCMAudio(
                    BytesIO(await self.synthesize("amitaro", "接続しました。")),
                    pipe=True,
                )
            )

    @app_commands.command(description="...")
    async def leave(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            await interaction.followup.send("接続していません。")
        else:
            self.connected_channels.remove(interaction.channel.id)
            await voice_client.disconnect()
            await interaction.followup.send("切断しました。")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if message.channel.id not in self.connected_channels:
            return
        voice_client = message.guild.voice_client
        if voice_client is None:
            self.connected_channels.remove(message.channel.id)
            return
        voice_client.play(
            discord.FFmpegPCMAudio(
                BytesIO(await self.synthesize("amitaro", message.content)), pipe=True
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TTS(bot))
