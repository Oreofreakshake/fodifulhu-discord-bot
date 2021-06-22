import discord
from discord import channel
from discord import message
from discord import embeds
from discord import errors
from discord.ext import commands

from discord.ext.commands.core import command
import cogs._json


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation Cog has been loaded....\n")

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
                description="`reason: `" + reason,
                colour=0xBF8040,
            )
            await channel.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "```really nigger? you don't have the balls to kick anyone, fag```"
            )

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def canyou(self, ctx):
        await ctx.send(
            f"```Can I what? be specific retard, refer to <prefix>help canyou ```"
        )

    @canyou.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)
        await ctx.send("```banned that motherfucker```")

        channel = self.bot.get_channel(841805435698020373)
        embed = discord.Embed(
            title=f"{ctx.author.name} banned: {member.name}",
            description="`reason: `" + reason,
            colour=0xBF8040,
        )
        await channel.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "```really nigger? you don't have the balls to ban anyone, fag```"
            )

    @canyou.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)
        await ctx.send("`ok`")

        channel = self.bot.get_channel(841805435698020373)
        embed = discord.Embed(
            title=f"{ctx.author.name} unbanned: {member.name}",
            description="`reason: `" + reason,
            colour=0xBF8040,
        )
        await channel.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "```if you can't ban niggers then you obviously can't unban niggers, dumbass```"
            )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def cls(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount + 1)
        channel = self.bot.get_channel(ctx.channel.id)

        embed = discord.Embed(
            title=f"{ctx.author.name} cleared: {ctx.channel.name}",
            description=f"{amount} messages were deleted",
            colour=0xBF8040,
        )

        await channel.send(embed=embed)

    @cls.error
    async def cls_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```delete your own messages, lazy gay looking fuck ```")


def setup(bot):
    bot.add_cog(Moderation(bot))