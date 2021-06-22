import discord
from discord import channel
from discord.abc import _Overwrites
from discord.ext import commands
from discord.ext.commands.core import command
from discord.permissions import PermissionOverwrite
import cogs._json


class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Cog has been loaded....\n")

    @commands.command(aliases=["cs"])
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx, channel: discord.TextChannel = None):

        channel = ctx.channel or channel
        embed = discord.Embed(
            title=f"```Stats for {channel.name}```",
            description=f"{'`Category : {}'.format(channel.category.name) if channel.category else 'this channel is not in the category'}`",
            colour=0xBF8040,
        )

        if channel.slowmode_delay == 0:
            slow_mode = "off"

        fields = [
            ("Channel Guild", ctx.guild.name, False),
            ("Channel ID", channel.id, False),
            ("Channel Topic", channel.topic, False),
            ("Channel Position", channel.position, False),
            ("Channel Slowmode Delay", slow_mode, False),
            ("Channel Creation time", channel.created_at, False),
        ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        await ctx.send(
            "i dont understand tf you trying to say, retard, try <prefix>help new"
        )

    @new.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(
            f"```I made a new category called {category.name} for you lazy fucker ```"
        )

    @new.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
        await ctx.send(
            f"```I made a new category called {channel.name} for you lazy fucker```"
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(
                f"```I want you all to shut the fuck up in {channel.name}```"
            )
        elif (
            channel.overwrites[ctx.guild.default_role].send_messages == True
            or channel.overwrites[ctx.guild.default_role].send_messages == None
        ):
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(
                f"```I want you all to shut the fuck up in {channel.name}```"
            )
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"```ok you can talk in {channel.name} now ```")


def setup(bot):
    bot.add_cog(Channel(bot))
