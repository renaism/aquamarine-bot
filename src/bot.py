import os
import discord
import logging
import random
import time

from dotenv import load_dotenv
from discord.ext import commands

from cogs.socialgame import SocialGame
from cogs.quiz.quiz import Quiz

class Bot(commands.Bot):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data


    async def on_ready(self):
        print(f"{self.user} is now connected to Discord.")

        print(f"\nConnected servers ({len(self.guilds)}):")
        for i, guild in enumerate(self.guilds):
            print(f"{i+1}. {guild.name} [{guild.id}]")


    @commands.command()
    async def ping(self, ctx):
        msg = random.choice([
            "Hahi~"
        ])

        await ctx.send(msg)


if __name__ == "__main__":
    # Logging setup
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    os.makedirs("logs", exist_ok=True)
    handler = logging.FileHandler(filename=f"logs/{time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))}.log", encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    logger.addHandler(handler)

    # Load environment variables
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    # Temporary data
    data = {
        "SocialGame": {},
        "Quiz": {}
    }

    bot = Bot(data, command_prefix="=")
    bot.add_cog(SocialGame(bot))
    bot.add_cog(Quiz(bot))
    bot.run(TOKEN)