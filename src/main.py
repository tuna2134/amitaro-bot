from discord.ext import commands
import discord

from dotenv import load_dotenv

from os import getenv
from logging import getLogger


logger = getLogger("amitaro")


class AmitaroBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        logger.info("Loaded jishaku")
        await self.load_extension("cogs.tts")


def main() -> None:
    load_dotenv()

    bot = AmitaroBot(command_prefix="ami!", intents=discord.Intents.all())

    bot.run(getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
