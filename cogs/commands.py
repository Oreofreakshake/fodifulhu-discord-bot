from sys import prefix
import discord
from discord import member
from discord import mentions
from discord import message
from discord.ext import commands
import platform
import datetime
from discord.ext.commands import bot
import random
from discord.ext.commands.core import command, is_owner
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
    @commands.is_owner()
    async def stats(self, ctx):
        pythonVersion = str(platform.python_version())
        dpyVersion = str(discord.__version__)
        serverCount = str(len(self.bot.guilds))
        memberCount = str(len(set(self.bot.get_all_members())))

        if serverCount != 1:
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

    @stats.error
    async def stats_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                "```this command for the time being is not allowed for you ```"
            )

    @commands.command(aliases=["fuckoff", "bye"])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Hey {ctx.author.mention} I'm going to sleep :sleeping:")
        await self.bot.logout()

    @logout.error
    async def logout_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send("```you dont have the permission, idiot```")

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("```bruh, you can't blacklist yourself```")
            return

        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"```I have blacklisted {user.name} for being an ass```")

    @blacklist.error
    async def blacklist_error(
        self, ctx: commands.Context, error: commands.errors
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send("```you dont have the power to blacklist people, asshole```")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"```I have removed {user.name} from the blacklist```")

    @unblacklist.error
    async def unblacklist_error(
        self, ctx: commands.Context, error: commands.errors
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                "```nigga, if you can't blacklist, what made you think you can unblacklist```"
            )

    @commands.command()
    async def say(self, ctx, *, message=None):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        message = (
            message or "refer to the help command, I don't understand what you mean"
        )
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
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre="."):
        data = cogs._json.read_json("prefix")
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, "prefix")
        await ctx.send(
            f"```server prefix is now {pre}\nuse {pre} to use the bot commands\nexample: {pre}hello\n\nto change the prefix again :\n{pre}prefix <the-prefix-you-want>\n\nor\n\n{pre}prefix to change it to back to default prefix which is .```"
        )


def setup(bot):
    bot.add_cog(Commands(bot))