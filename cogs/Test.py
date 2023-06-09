import logging
from discord.ext import commands, tasks

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.test.start()

    @tasks.loop(seconds=1)
    async def test(self) -> None:
        await self.bot.wait_until_ready()
        logging.info("Test")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Test(bot))