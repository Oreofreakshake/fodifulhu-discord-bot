from datetime import datetime
from discord import Intents, colour
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.errors import CommandNotFound

PREFIX = "."
OWNER_ID = [442629841716772864]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler

        super().__init__(
            command_prefix=PREFIX, owner_ids=OWNER_ID, intents=Intents.all()
        )

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("FodiFulhu is online")

    async def on_disconnect(self):
        print("FodiFulhu is disconnected")

    async def on_error(self, event_method, *args, **kwargs):
        if event_method == "on_command_error":
            await args[0].send("i think something is wrong")

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(585411891447463952)
            print("bot ready")

            channel = self.get_channel(836343738745356368)

            embed = Embed(
                title="I'm online",
                description="but you cant use any commands atm",
                colour=0xBF8040,
                timestamp=datetime.utcnow(),
            )

            fields = [
                ("progress -->", "adding basic commands", True),
                ("modifying embed", ">1", False),
                ("error handling", ">2", False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text="online since")

            await channel.send(embed=embed)
        else:
            print("bot reconnected")

    async def on_message(self):
        pass


bot = Bot()