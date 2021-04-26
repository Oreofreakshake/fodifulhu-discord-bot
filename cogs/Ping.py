<<<<<<< HEAD
import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"pong your ping is")


def setup(bot):
    bot.add_cog(Ping(bot))
=======
import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"pong your ping is")


def setup(bot):
    bot.add_cog(Ping(bot))
>>>>>>> 8156af3c03ff11093505737b89eff5ec1d16ebc3
