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
from discord.ext.commands.errors import CommandOnCooldown

from discord.flags import alias_flag_value


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n------")

secrete_file = json.load(open(cwd + "/bot_config/secrets.json"))

bot = commands.Bot(
    command_prefix=".", case_insenstive=True, owner_id="442629841716772864"
)
bot.config_token = secrete_file["token"]
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []


@bot.event
async def on_ready():
    print(
        "-------\nLogged in as: {} : {}\n-------\nprefix = .\n-------".format(
            bot.user.name, bot.user.id
        )
    )

    await bot.change_presence(activity=discord.Game(name=f"use . to interact with me"))


@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, CommandOnCooldown):
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
        descrition="\uFEFF",
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
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@stats.error
async def stats_error(ctx, error):
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


@bot.command()
async def say(ctx, *, message=None):
    message = message or "refer to the help command, I don't understand what you mean"
    await ctx.message.delete()
    await ctx.send(f"`{message}`")


@bot.command()
async def saam(ctx):
    await ctx.send(
        "`did you just try to use the saam command? you fucking gay black piece of shit ass hair, go kys`"
    )


bot.run(bot.config_token)