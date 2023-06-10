import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!don"), 
    intents=discord.Intents.all(),
    description="LIMBUS COMPANYYY!!!")
bot.remove_command('help')

@bot.event
async def on_ready() -> None:
    logging.info("Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(
        "LIMBUS COMPANYYY!!!"
    ))

if __name__ == "__main__":
    if TOKEN is None:
        logging.error("TOKEN is None")
        exit(1)

    bot.load_extension("cogs.MorningCog")
    bot.load_extension("cogs.LimbusCog")
    bot.load_extension("cogs.VoiceCog")
    bot.run(TOKEN)