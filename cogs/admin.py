import discord
from discord import channel
from discord.ext import commands
import platform
import datetime

from discord.ext.commands.core import command
import cogs._json


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation Cogs has been loaded....\n")

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
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre="."):
        data = cogs._json.read_json("prefix")
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, "prefix")
        await ctx.send(
            f"```server prefix is now {pre}\nuse {pre} to use the bot commands\nexample: {pre}hello\n\nto change the prefix again :\n{pre}prefix <the-prefix-you-want>\n\nor\n\n{pre}prefix to change it to back to default prefix which is .```"
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.message.author.id == member.id:
            await ctx.send("```you cant kick yourself, retard ```")
            return
        else:
            await ctx.guild.kick(user=member, reason=reason)
            await ctx.send("```kicked that motherfucker```")

            channel = self.bot.get_channel(841805435698020373)
            embed = discord.Embed(
                title=f"{ctx.author.name} kicked: {member.name}",
                description=reason,
                colour=0xBF8040,
            )
            await channel.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "```really nigger? you don't have the balls to kick anyone, fag```"
            )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)
        await ctx.send("```banned that motherfucker```")

        channel = self.bot.get_channel(841805435698020373)
        embed = discord.Embed(
            title=f"{ctx.author.name} banned: {member.name}",
            description=reason,
            colour=0xBF8040,
        )
        await channel.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "```really nigger? you don't have the balls to ban anyone, fag```"
            )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)
        await ctx.send("`ok`")

        channel = self.bot.get_channel(841805435698020373)
        embed = discord.Embed(
            title=f"{ctx.author.name} unbanned: {member.name}",
            description=reason,
            colour=0xBF8040,
        )
        await channel.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "```if you can't ban niggers then you obviously can't unban niggers, dumbass```"
            )


def setup(bot):
    bot.add_cog(Moderation(bot))