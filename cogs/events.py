from base64 import decodebytes
import discord
from discord import embeds
from discord.ext import commands
import random
import datetime


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded....\n")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="recording")
        if channel:
            embed = discord.Embed(decription="Welcome to boakibaa", colour=0xBF8040)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)

            if int(h) == 0 and int(m) == 0:
                await ctx.send(f"you must wait {int(s)} seconds to use this command!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f"you must wait {int(m)} minutes, {int(s)} seconds to use this command!"
                )
            else:
                await ctx.send(
                    f"you must wait {int(h)}hours, {int(m)} minutes, {int(s)} seconds to use this command!"
                )
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.send(
                "I don't understand what you mean, can you refer to the help command"
            )
        raise error


def setup(bot):
    bot.add_cog(Events(bot))