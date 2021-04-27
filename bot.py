import discord
from discord import activity
from discord import member
from discord.embeds import Embed
from discord.ext import commands
import logging
from pathlib import Path
import platform
import json
from datetime import datetime

from discord.flags import alias_flag_value


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n------")

secrete_file = json.load(open(cwd + "/bot_config/secrets.json"))

bot = commands.Bot(command_prefix=".", case_insenstive=True)
bot.config_token = secrete_file["token"]
logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
    print(
        "-------\nLogged in as: {} : {}\n-------\nprefix = .\n-------".format(
            bot.user.name, bot.user.id
        )
    )

    await bot.change_presence(activity=discord.Game(name=f"use . to interact with me"))


@bot.command(name="hi", aliases=["hello"])
async def _hi(ctx):
    await ctx.send(f"Hi {ctx.author.mention}!")


@bot.command()
@commands.is_owner()
async def stats(ctx):
    pythonVersion = str(platform.python_version())
    dpyVersion = str(discord.__version__)
    serverCount = str(len(bot.guilds))
    memberCount = str(len(set(bot.get_all_members())))

    if serverCount != 1:
        guilds = " guilds"
    else:
        guilds = " guild"

    embed = Embed(
        title="myStatus",
        descrition="------------",
        colour=0xBF8040,
        timestamp=datetime.utcnow(),
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

    await ctx.send(embed=embed)


@stats.error
async def status_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"you dont have permission, idiot{ctx.author.mention}")


@bot.command(aliases=["fuckoff", "bye"])
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f"Hey {ctx.author.mention} I'm logging out :wave:")
    await bot.logout()


@logout.error
async def logout_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"you dont have the permission, idiot {ctx.author.mention}")
    else:
        raise error


bot.run(bot.config_token)