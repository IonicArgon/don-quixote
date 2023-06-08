import toml
import logging
import asyncio
import typing
import discord
from discord.ext import commands

class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = toml.load("config.toml")
        self.general_channels = None

    async def base_on_ready(self) -> None:
        self.general_channels = self.find_general_channel()

    async def find_general_channel(self) \
    -> typing.Optional[discord.TextChannel]:
        logging.info("Looking for general channels")

        async for guild in self.bot.fetch_guilds():
            channels_raw = await guild.fetch_channels()
            def filter_(channel):
                if type(channel) == discord.TextChannel:
                    return channel
            channels = list(filter(filter_, channels_raw))
            channel = None

            logging.info(f'Checking guild {guild.id}')
            logging.info("Searching for guild in config.toml")
            
            for general_channel in self.config["general_channels"]:
                if general_channel["guild_id"] == guild.id:
                    logging.info("Found guild")
                    logging.info("Searching for channel in guild")

                    general_channel_ = general_channel["channel_id"]
                    for channel_ in channels:
                        if channel_.id == general_channel_:
                            logging.info(f"Found channel {channel_.id}")
                            channel = channel_
                            break
                    break
            
            if channel is None:
                logging.info("No configured channel found for guild, defaulting to first channel")
                channel = channels[0]

            yield channel