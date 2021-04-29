import re
import os
import discord
from discord import activity
from discord import member
from discord.embeds import Embed
from discord.ext import commands
import logging
from pathlib import Path
import json


from discord.flags import alias_flag_value


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n------")

secrete_file = json.load(open(cwd + "/bot_config/secrets.json"))

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    case_insenstive=True,
    owner_id=442629841716772864,
)
bot.config_token = secrete_file["token"]
logging.basicConfig(level=logging.INFO)

bot.version = "0.0.5"

bot.blacklisted_users = []
bot.cwd = cwd


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
    if ctx.message.author.id in bot.blacklisted_users:
        return
    await ctx.send(f"Hi {ctx.author.menion}!")


@bot.command(aliases=["fuckoff", "bye"])
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f"Hey {ctx.author.mention} I'm logging out :wave:")
    await bot.logout()


if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)