from discord.ext import commands


class Invite:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self):
        await self.bot.say(":tada: https://discordapp.com/oauth2/authorize?permissions=0&client_id=377448422841516032&scope=bot")


def setup(bot):
    bot.add_cog(Invite(bot))
