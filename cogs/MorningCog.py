import discord
import typing
import logging
import time
import toml
from discord.ext import commands, tasks

class MorningCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = toml.load("config.toml")
        self.announced_morning = False

        self.reset_announced_morning.start()
        self.valorous_morning.start()

    def cog_unload(self) -> None:
        self.valorous_morning.cancel()

    async def find_general_channel(self) \
    -> typing.Optional[discord.TextChannel]:
        if self.config["general"] != 0:
            logging.info("Using channel ID from config.toml")
            return self.bot.get_channel(self.config["general"])

        logging.info("Using default channel search")
        for channel in self.bot.get_all_channels():
            logging.info(f'Checking channel {channel.name} of type {type(channel)}')
            if type(channel) is not discord.channel.TextChannel:
                continue

            if "general" not in channel.name.lower():
                continue

            logging.info(f'Found general channel {channel.name}')
            return channel
        
        return None
    
    @tasks.loop(seconds=15)
    async def reset_announced_morning(self) -> None:
        await self.bot.wait_until_ready()
        time_now = time.localtime()
        if time_now.tm_hour != self.config["morning_hour"]:
            self.announced_morning = False
    
    @tasks.loop(minutes=1)
    async def valorous_morning(self) -> None:
        await self.bot.wait_until_ready()
        channel = await self.find_general_channel()

        if channel is None:
            logging.error("Could not find general channel")
            return
        
        time_now = time.localtime()
        if time_now.tm_hour != self.config["morning_hour"]:
            logging.info("Not morning yet")
            return
        
        if self.announced_morning:
            logging.info("Already announced morning")
            return
        
        title = "Valorous morning!"
        description = "\'Tis time to riseth and grindeth!"
        footer = "Bot by .extro"

        embed = discord.Embed(
            title=title,
            description=description,
            color=int("FFEF23", 16)
        ).set_image(
            url="https://media.tenor.com/vqKSSrOw4yYAAAAC/glitter-limbus-company.gif"
        ).set_footer(
            text=footer
        )

        self.announced_morning = True
        await channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MorningCog(bot))
