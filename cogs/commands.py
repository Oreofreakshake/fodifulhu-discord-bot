import discord
from discord.ext import commands
import platform
import datetime

from discord.ext.commands.core import is_owner
import cogs._json


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded....\n")

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

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("`bruh, you can't blacklist yourself`")
            return

        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json(self.bot.blacklisted_users, "blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"`I have blacklisted {user.name} for being an ass `")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json(self.bot.blacklisted_users, "blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"`I have removed {user.name} from the blacklist`")

    @commands.command()
    async def say(self, ctx, *, message=None):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        message = (
            message or "refer to the help command, I don't understand what you mean"
        )
        await ctx.message.delete()
        await ctx.send(f"`{message}`")

    @commands.command()
    async def saam(self, ctx):
        if ctx.message.author.id in self.bot.blacklisted_users:
            return
        else:
            await ctx.send(
                "`did you just try to use the saam command? you fucking gay black piece of shit ass hair, go kys`"
            )


def setup(bot):
    bot.add_cog(Commands(bot))