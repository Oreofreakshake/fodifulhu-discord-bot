import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            color=discord.Colour.green())
        embed.set_author(name='Help : list of commands available')
        embed.add_field(
            name='.ping', value='Returns bot respond time in milliseconds', inline=False)
        embed.add_field(
            name='.say', value='Replies to any argument you provide after the command, try an example ".say hello" ', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
