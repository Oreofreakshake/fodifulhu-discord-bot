import discord
from discord.ext import commands
import random
import cogs._json


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games Cog has been loaded....\n")

    @commands.command()
    async def saamometer(self, ctx, user: discord.Member):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        values = []
        for i in range(101):
            values.append(i)
            rand = random.choice(values)

        if ctx.message.author.id == user.id:
            await ctx.send(
                "```tag other members, if you want to check how much of a black ass nigger saam you are, just try .saamometer```"
            )
            return

        if user.mention == "<@!484029862474940426>":
            await ctx.send(
                f"```saam obviously is the glorious black ass nigger saam```"
            )
        else:
            await ctx.send(f"{user.mention} is {rand}% saam")

    @saamometer.error
    async def saamometer_error(
        self, ctx: commands.Context, error: commands.errors
    ) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            values = []
            for i in range(101):
                values.append(i)
                rand = random.choice(values)
            await ctx.send(f"```you are {rand}% saam```")


def setup(bot):
    bot.add_cog(Games(bot))