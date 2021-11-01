from base64 import decodebytes
import discord
from discord import embeds
from discord.ext import commands
import random
import datetime

from requests.models import Response


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded....\n")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(585411891447463956)

        response = [
            f"Hopefully you wont regret joining {member.name}",
            f"this is pretty much a really dead ass server but welcome {member.name}",
            f"Enjoy the stay {member.name}",
            f"This isnt a server for you if you easily can get offended, but welcome {member.name}",
            f"I am not the admin bot, im just very based, hope you enjoy the stay {member.name}",
            f"Retarded server but ok, have some fun {member.name}",
            f"Oh i didnt notice you there, {member.name}, JK i did, dw im not your dad",
        ]

        embed = discord.Embed(description=(random.choice(response)), colour=0xBF8040)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = self.bot.get_channel(585411891447463956)

        response = [
            f"lol, pussy {member.name}",
            f"no one really wanted you to stay here anyway {member.name}",
            f"got offended and left to cry?, {member.name}",
            f"aw you didnt get personal suck jobs from saam? lgbtq+ ass",
            f"some corny dude aka, {member.name} left",
            f"{member.name} was a pain in the asshole anyway",
        ]
        embed = discord.Embed(
            description=(random.choice(response)),
            colour=0xBF8040,
        )
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
                await ctx.send(
                    f"```you must wait {int(s)} seconds to use this command!```"
                )
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f"```you must wait {int(m)} minutes, {int(s)} seconds to use this command!```"
                )
            else:
                await ctx.send(
                    f"```you must wait {int(h)}hours, {int(m)} minutes, {int(s)} seconds to use this command!```"
                )
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.send(
                "```I don't understand what you mean, can you refer to the help command```"
            )
        raise error


def setup(bot):
    bot.add_cog(Events(bot))
