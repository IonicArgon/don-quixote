import discord
import logging
import datetime
import pytz
from typing import cast
from astral.geocoder import database, lookup
from astral.sun import sun
from astral import LocationInfo
from enum import Enum
from discord.ext import commands, tasks
from cogs.BaseCog import BaseCog

class TimeOfDay(Enum):
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2
    NIGHT = 3

class LimbusCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.location = cast(LocationInfo, lookup("New York", database()))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.base_on_ready()
        self.manager_esquire.start()
        logging.debug("LimbusCog initialized")
    
    @tasks.loop(seconds=1)
    async def manager_esquire(self) -> None:
        await self.bot.wait_until_ready()

        logging.debug("Checking for manager esquires")

        if self.general_channels is None:
            logging.debug("General channels are not ready")
            return
        
        time_of_day = await self.get_time_of_day()
        description = None
        if time_of_day == TimeOfDay.MORNING:
            description = self.config["greetings"]["morning"]
        elif time_of_day == TimeOfDay.AFTERNOON:
            description = self.config["greetings"]["afternoon"]
        elif time_of_day == TimeOfDay.EVENING:
            description = self.config["greetings"]["evening"]
        elif time_of_day == TimeOfDay.NIGHT:
            description = self.config["greetings"]["night"]

        for guild, channel, _ in self.general_channels:
            for member in guild.members:
                if member.bot:
                    continue

                if self.member_activity_check(member):
                    logging.debug(f'Found manager esquire {member.name}')
                    embed = discord.Embed(
                        title=f'MANAGER ESQUIRE {member.display_name.upper()}!!!',
                        description=description,
                        color=0xFFEF23) \
                        .set_image(url="https://media.tenor.com/aYgU4nM0CHUAAAAC/don-quixote-limbus-company.gif") \
                        .set_footer(text="Bot by .extro")
                
                    await channel.send(member.mention, embed=embed)

    async def get_time_of_day(self) -> TimeOfDay:
        now = datetime.datetime.now(pytz.utc) \
            .astimezone(pytz.timezone(self.location.timezone))
        sun_ = sun(self.location.observer, date=now)
        if sun_["sunrise"] < now < sun_['noon']:
            return TimeOfDay.MORNING
        elif sun_["noon"] <= now < sun_['sunset']:
            return TimeOfDay.AFTERNOON
        elif sun_["sunset"] <= now < sun_['dusk']:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT

def setup(bot: commands.Bot) -> None:
    bot.add_cog(LimbusCog(bot))