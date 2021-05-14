from sys import prefix
import discord
from discord import member
from discord import mentions
from discord import message
from discord.ext import commands
from discord.ext.commands import bot
import random
from discord.ext.commands.core import command, is_owner
import platform
import datetime
import cogs._json


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded....\n")

    @commands.command(aliases=["hello", "test"])
    async def hi(self, ctx):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        await ctx.send(f"yes I am alive {ctx.author.mention}!")

    @commands.command()
    async def stats(self, ctx):
        pythonVersion = str(platform.python_version())
        dpyVersion = str(discord.__version__)
        serverCount = str(len(self.bot.guilds))
        memberCount = str(ctx.guild.member_count)

        if serverCount != "1":
            guilds = " guilds"
        else:
            guilds = " guild"

        embed = discord.Embed(
            title="myStatus",
            descrition="\uFEFF",
            colour=0xBF8040,
            timestamp=datetime.datetime.utcnow(),
        )

        fields = [
            ("No. servers ", "I am in " + serverCount + guilds, True),
            ("No. members", memberCount, False),
            ("Python version", pythonVersion, False),
            ("Discord version", dpyVersion, False),
        ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Online since: ")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *, message=None):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        message = message or "nigger, say something or check the help command, dumbass"
        await ctx.message.delete()
        await ctx.send(f"```{message}```")

    @commands.command()
    async def saam(self, ctx, user: discord.Member):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        responses = [
            " just had rough sex with saam",
            " sucked saam's dick while he was peeing",
            " licked saams unshaved 8ball looking ass",
            " played with saam's ball last night",
            " ate saam's kess while licking the cum off from saam's black wet dick",
            ' role played "two girls one cup" with saam',
            " licked inside saam's butthole",
        ]
        if ctx.message.author.id == user.id:
            await ctx.send(
                "```nigger, why tf you wanna have sex with saam yourself?```"
            )
            return

        if not user.bot:
            await ctx.send(f"{user.mention}{random.choice(responses)}")
            return

        else:
            await ctx.send(
                "```Saam can't fuck with bots you dumb black jew looking fuck```"
            )

    @saam.error
    async def saam_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "```did you just try to use the saam command? you fucking gay black piece of shit ass hair, go kys```"
            )

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        ping_value = round(self.bot.latency * 1000)
        if ping_value <= 100:
            await ctx.send(
                f"```damn nigger, my internet speed is kinda epic -> {ping_value}ms```"
            )
        else:
            await ctx.send(f"```fuck this shit, slow ass internet -> {ping_value}ms```")


def setup(bot):
    bot.add_cog(Commands(bot))