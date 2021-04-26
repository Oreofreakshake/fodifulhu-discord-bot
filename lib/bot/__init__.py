from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "."
OWNER_ID = [442629841716772864]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_ID)

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

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(585411891447463952)
            print("bot ready")
        else:
            print("bot reconnected")

    async def on_message(self):
        pass


bot = Bot()