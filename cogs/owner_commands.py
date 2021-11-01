import discord
from discord.ext import commands

import cogs._json


class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Command Cogs has been loaded....\n")

    @commands.command(aliases=["fuckoff", "bye"])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Hey {ctx.author.mention} I'm going to sleep :sleeping:")
        await self.bot.logout()

    @logout.error
    async def logout_error(self, ctx: commands.Context, error: commands.errors) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send("```you dont have the permission, idiot```")

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("```bruh, you can't blacklist yourself```")
            return

        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"```I have blacklisted {user.name} for being an ass```")

    @blacklist.error
    async def blacklist_error(
        self, ctx: commands.Context, error: commands.errors
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send("```you dont have the power to blacklist people, asshole```")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"```I have removed {user.name} from the blacklist```")

    @unblacklist.error
    async def unblacklist_error(
        self, ctx: commands.Context, error: commands.errors
    ) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                "```if you can't blacklist, what made you think you can unblacklist, dumbass```"
            )


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
