import discord
import logging
import time
from discord.ext import commands, tasks
from cogs.BaseCog import BaseCog

class MorningCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.morning_hour = self.config["morning_hour"]
        self.current_hour = None
        self.announced_morning = False

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.base_on_ready()
        self.morning_announcement.start()
        self.reset_annoucements.start()
        logging.debug("MorningCog initialized")

    @tasks.loop(seconds=1)
    async def reset_annoucements(self) -> None:
        await self.bot.wait_until_ready()
        if self.announced_morning and self.current_hour != self.morning_hour:
            self.announced_morning = False
            logging.debug("Reset morning announcement")
    
    @tasks.loop(seconds=1)
    async def morning_announcement(self) -> None:
        await self.bot.wait_until_ready()
        self.current_hour = time.localtime().tm_hour

        if not self.general_channels:
            logging.debug("General channels not ready")
            return

        if not self.announced_morning:
            if self.current_hour == self.morning_hour:
                logging.debug("Morning time")
                self.announced_morning = True
                await self.announce_morning()

    async def announce_morning(self) -> None:
        logging.debug("Announcing morning")
        embed = discord.Embed(
            title="Valorous morning!",
            description="\'Tis time to **riseth** and **grindeth!**",
            color=0xFFEF23) \
            .set_image(url="https://media.tenor.com/vqKSSrOw4yYAAAAC/glitter-limbus-company.gif") \
            .set_footer(text="Bot by .extro")
        
        if self.general_channels is None:
            logging.debug("General channels not ready")
            return
        
        for _, channel, _ in self.general_channels:
            await channel.send(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(MorningCog(bot))