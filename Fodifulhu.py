<<<<<<< HEAD
import os
import random

import discord
from discord.ext import commands

TOKEN = open("token.txt", "r").readline()

bot = commands.Bot(command_prefix=".")
bot.remove_command("help")


bot.load_extension(f"cogs.Ping")


bot.load_extension(f"cogs.Help")


@commands.command()
async def say(ctx, *args):

    if len(args) > 0:
        await ctx.send(" ".join(args))
    else:
        await ctx.send(f"refer to the help command")


bot.add_command(say)


@bot.command()
async def add_command():
    bot.add_command(help)


bot.run(TOKEN)
=======
import os
import random

import discord
from discord.ext import commands

TOKEN = open("token.txt", "r").readline()

bot = commands.Bot(command_prefix=".")
bot.remove_command("help")


bot.load_extension(f"cogs.Ping")


bot.load_extension(f"cogs.Help")


@commands.command()
async def say(ctx, *args):

    if len(args) > 0:
        await ctx.send(" ".join(args))
    else:
        await ctx.send(f"refer to the help command")


bot.add_command(say)


@bot.command()
async def add_command():
    bot.add_command(help)


bot.run(TOKEN)
>>>>>>> 8156af3c03ff11093505737b89eff5ec1d16ebc3
