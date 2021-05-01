import re
import os
from sys import prefix
import discord
from discord import activity
from discord import member
from discord.embeds import Embed
from discord.ext import commands
import logging
from pathlib import Path
import json
import cogs._json

from discord.flags import alias_flag_value


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n------")


def get_prefix(bot, messgae):
    data = cogs._json.read_json("prefix")
    if not str(messgae.guild.id) in data:
        return commands.when_mentioned_or(".")(bot, messgae)
    return commands.when_mentioned_or(data[str(messgae.guild.id)])(bot, messgae)


secrete_file = json.load(open(cwd + "/bot_config/secrets.json"))

bot = commands.Bot(
    command_prefix=get_prefix,
    case_insenstive=True,
    owner_id=442629841716772864,
)
bot.config_token = secrete_file["token"]
logging.basicConfig(level=logging.INFO)

bot.version = "6"

bot.blacklisted_users = []
bot.cwd = cwd


@bot.event
async def on_ready():
    print(
        "-------\nLogged in as: {} : {}\n-------\nDeveloper : boakibaa#9764 : 442629841716772864\n-------".format(
            bot.user.name, bot.user.id
        )
    )

    await bot.change_presence(activity=discord.Game(name=f"use . to interact with me"))


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if message.author.id in bot.blacklisted_users:
        return
    if f"<@!{bot.user.id}" in message.content:
        data = cogs._json.read_json("prefix")
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = "."
        prefixMsg = await message.channel.send(f"```retard my prefix is {prefix}```")
        await prefixMsg.add_reaction("🖕")

    await bot.process_commands(message)


if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)