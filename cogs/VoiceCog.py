import discord
import logging
import typing
from discord.ext import commands, tasks
from cogs.BaseCog import BaseCog

class VoiceCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.voice_clients: list[typing.Optional[discord.VoiceClient]] = []

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.base_on_ready()
        await self.populate_voice_client_list()
        self.connect_disconnect_process.start()
        self.voice_loop.start()
        logging.debug("VoiceCog initialized")

    @tasks.loop(seconds=1)
    async def voice_loop(self) -> None:
        await self.bot.wait_until_ready()
        if self.general_channels is not None:
            for i in range(len(self.general_channels)):
                _, _, voice = self.general_channels[i]
                voice_client = self.voice_clients[i]

                if voice_client is None:
                    logging.debug("No voice client to play audio")
                    continue

                for member in voice.members:
                    if member.bot or voice_client.is_playing():
                        continue

                    if self.member_activity_check(member):
                        logging.debug(f'{member.activities}')
                        logging.debug(f"Playing audio for {member.display_name}")
                        voice_client.play(discord.FFmpegPCMAudio(
                            source=str(self.config["limbus_source"]),
                            executable=str(self.config["ffmpeg_path"])
                            ))

    @tasks.loop(seconds=1)
    async def connect_disconnect_process(self) -> None:
        await self.bot.wait_until_ready()
        if self.general_channels is not None:
            for i in range(len(self.general_channels)):
                _, _, voice = self.general_channels[i]

                if voice.members and self.voice_clients[i] is None:
                    logging.debug("Connecting to voice channel")
                    self.voice_clients[i] = await voice.connect()
                elif len(voice.members) < 2 and self.voice_clients[i] is not None:
                    logging.debug("Disconnecting from voice channel")
                    await self.voice_clients[i].disconnect() # type: ignore
                    self.voice_clients[i] = None
                else:
                    logging.debug("No voice client to connect/disconnect")

    async def populate_voice_client_list(self) -> None:
        await self.bot.wait_until_ready()
        if self.general_channels is not None:
            self.voice_clients = [None for _ in range(len(self.general_channels))]
            logging.debug(f'{self.voice_clients}')

def setup(bot: commands.Bot) -> None:
    bot.add_cog(VoiceCog(bot))