import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!don"), 
    intents=intents,
    description="LIMBUS COMPANYYY!!!")
bot.remove_command('help')

@bot.event
async def on_ready() -> None:
    logging.info("Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(
        "LIMBUS COMPANYYY!!!"
    ))

@bot.event
async def setup_hook() -> None:
    await bot.load_extension("cogs.MorningCog")

if __name__ == "__main__":
    if TOKEN is not None:
        bot.run(TOKEN)
    else:
        logging.error("No token found")
