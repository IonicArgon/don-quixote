import discord
import logging
import time
from discord.ext import commands, tasks
from cogs.BaseCog import BaseCog

class MorningCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.morning_hour = self.config["morning_hour"]
        self.announced_morning = False

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.base_on_ready()
        self.reset_annoucements.start()
        self.morning_announcement.start()
        logging.info("MorningCog ready")

    @tasks.loop(seconds=5)
    async def reset_annoucements(self) -> None:
        if self.announced_morning:
            self.announced_morning = False
            logging.info("Reset morning announcement")
    
    @tasks.loop(minutes=1)
    async def morning_announcement(self) -> None:
        if not self.announced_morning:
            current_time = time.localtime()
            if current_time.tm_hour == self.morning_hour:
                logging.info("Morning time")
                self.announced_morning = True
                await self.announce_morning()

    async def announce_morning(self) -> None:
        logging.info("Announcing morning")
        embed = discord.Embed(
            title="Valorous morning!",
            description="\'Tis time to **riseth** and **grindeth!**",
            color=int("FFEF23", 16)) \
            .set_image(url="https://images-ext-1.discordapp.net/external/12Md-q7qdrsMLTOuUuaIX-g1KgrQnfP4DFFGQNiycnA/https/media.tenor.com/vqKSSrOw4yYAAAAC/glitter-limbus-company.gif?width=448&height=448") \
            .set_footer(text="Bot by .extro")
        
        async for channel in self.general_channels:
            await channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MorningCog(bot))