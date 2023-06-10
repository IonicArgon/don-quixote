import toml
import logging
import typing
import discord
from discord.ext import commands

class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = toml.load("config.toml")
        self.general_channels = None
        self.member_storage = []
        self.GAME = "limbus"

    async def base_on_ready(self) -> None:
        self.general_channels = await self.find_general_channels()
        logging.debug("BaseCog initialized")

    async def find_general_channels(self) \
    -> list[tuple[discord.Guild, discord.TextChannel, discord.VoiceChannel]]:
        logging.debug("Looking for general channels")
        return_list = []

        for guild in self.bot.guilds:
            channels_raw = guild.channels
            voices_raw = guild.voice_channels
            def filter_(channel):
                if type(channel) == discord.TextChannel or type(channel) == discord.VoiceChannel:
                    return channel
            channels = list(filter(filter_, channels_raw))
            voices = list(filter(filter_, voices_raw))

            channel = None
            voice = None

            logging.debug(f'Checking guild {guild.id}')
            logging.debug("Searching for guild in config.toml")
            
            for general_channel in self.config["general_channels"]:
                if general_channel["guild_id"] == guild.id:
                    logging.debug("Found guild")
                    logging.debug("Searching for channel in guild")

                    general_channel_ = general_channel["channel_id"]
                    voice_channel = general_channel["voice_id"]

                    for channel_ in channels:
                        if channel_.id == general_channel_:
                            logging.debug(f"Found channel {channel_.id}")
                            channel = channel_
                            break

                    for voice_ in voices:
                        if voice_.id == voice_channel:
                            logging.debug(f"Found voice channel {voice_.id}")
                            voice = voice_
                            break
                    break
            
            if channel is None:
                logging.debug("No configured channel found for guild, defaulting to first channel")
                channel = channels[0]

            if voice is None:
                logging.debug("No configured voice channel found for guild, defaulting to first voice channel")
                voice = voices[0]

            return_list.append((guild, channel, voice))

        return return_list

    async def guild_members_generator(self, guild: discord.Guild) \
    -> typing.AsyncGenerator[discord.Member, None]:
        logging.debug("Looking for guild members")

        async for member in guild.fetch_members():
            yield member

    def member_activity_check(self, member: discord.Member) -> bool:
        if len(member.activities) == 0:
            logging.debug(f"{member.name} is not playing anything")
            return False

        for activity in member.activities:
            logging.debug(f"{member.name} is playing {activity.name}")

            if activity.name is None:
                continue
            
            if self.GAME in activity.name.lower() and activity.type == discord.ActivityType.playing:
                if member not in self.member_storage:
                    self.member_storage.append(member)
                    return True
                else:
                    return False
            
        if member in self.member_storage:
            self.member_storage.remove(member)
        return False

def setup(bot: commands.Bot) -> None:
    bot.add_cog(BaseCog(bot))
