import re
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
from discord.ext.commands.errors import CheckFailure, CommandOnCooldown
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


@bot.event
async def on_ready():
    print(
        "-------\nLogged in as: {} : {}\n-------\nprefix = .\n-------".format(
            bot.user.name, bot.user.id
        )
    )

    data = read_json(bot.blacklisted_users, filename="blacklist")
    bot.blacklisted_users = data["blacklistedUsers"]

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


@bot.command()
@commands.is_owner()
async def blacklist(ctx, user: discord.Member):
    if ctx.message.author.id == user.id:
        await ctx.send("`bruh, you can't blacklist yourself`")
        return

    bot.blacklisted_users.append(user.id)
    data = read_json(bot.blacklisted_users, "blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"`I have blacklisted {user.name} for being an ass `")


@blacklist.error
async def blacklist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("`LOL you don't have the power to blacklist anyone, peasant`")


@bot.command()
@commands.is_owner()
async def unblacklist(ctx, user: discord.Member):
    bot.blacklisted_users.remove(user.id)
    data = read_json(bot.blacklisted_users, "blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"`I have removed {user.name} from the blacklist`")


@unblacklist.error
async def unblacklist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("`you can't unblacklist if you can't blacklist, dumbass`")


@bot.command(name="hi", aliases=["hello"])
async def _hi(ctx):
    if ctx.message.author.id in bot.blacklisted_users:
        return
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
    if ctx.message.author.id in bot.blacklisted_users:
        return
    message = message or "refer to the help command, I don't understand what you mean"
    await ctx.message.delete()
    await ctx.send(f"`{message}`")


@bot.command()
async def saam(ctx):
    if ctx.message.author.id in bot.blacklisted_users:
        return
    await ctx.send(
        "`did you just try to use the saam command? you fucking gay black piece of shit ass hair, go kys`"
    )


def read_json(data, filename):
    with open(f"{cwd}/blacklist_config/{filename}.json", "r") as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    with open(f"{cwd}/blacklist_config/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


bot.run(bot.config_token)