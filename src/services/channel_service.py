from discord import Channel, Message
from discord.ext.commands import Context
from ..bunkbot import BunkBot
from ..models.service import Service
from ..services.database_service import DatabaseService
from ..services.error_log_service import ErrorLogService
from ..util.constants import CHANNEL_GENERAL, CHANNEL_BOT_LOGS, CHANNEL_BOT_TESTING

EXCLAMATION: str = ":exclamation:"
ROBOT: str = ":robot:"

"""
Service responsible for handling channel references
"""
class ChannelService(Service):
    def __init__(self, bot: BunkBot, database: DatabaseService, logger: ErrorLogService):
        super().__init__(bot, database)
        self.BOT_TESTING: Channel = None
        self.BOT_LOGS: Channel = None
        self.GENERAL: Channel = None
        self.WEATHER: Channel = None
        self.MOD_CHAT: Channel = None
        self.logger: ErrorLogService = logger

    # locate specific channels setup through
    # user and code config
    async def load(self) -> None:
        await super().load()

        self.BOT_LOGS = await self.get(CHANNEL_BOT_LOGS)
        self.BOT_TESTING = await self.get(CHANNEL_BOT_TESTING)
        self.bot.on_error += self.log_error

        await self.bot.send_message(self.BOT_LOGS, "{0} Bot loaded {1}".format(ROBOT, ROBOT))

    # log a simple information message to 
    # the bot logs channel
    async def log_info(self, message: str) -> None:
        try:
            await self.bot.send_message(self.BOT_LOGS, message)
        except Exception as e:
            self.logger.log_error(e)

    # log an error in the bot_logs channel when
    # BunkBot emits the error event
    async def log_error(self, error: Exception, command: str, ctx: Context) -> None:
        try:
            error_message: str = ":exclamation: Error occurred from command '{0}': {1}".format(command, error)

            if ctx is not None:
                msg: Message = ctx.message
                err: str = "{0} An error has occurred! {0} @fugwenna help ahhhh".format(EXCLAMATION, EXCLAMATION)
                await self.bot.say_to_channel(msg.channel, err)

            await self.bot.say_to_channel(self.BOT_LOGS, error_message)
        except Exception as e:
            self.logger.log_error(e)

    # get an instance of a
    # channel based on the given name - if
    # no name is specified, the general chat is assumed
    async def get(self, name: str) -> Channel:
        return next(c for c in self.server.channels if c.name == name)

    # send the 'typing' event to a channel based on a context message
    async def start_typing(self, ctx: Context) -> None:
        await self.bot.send_typing(ctx.message.channel)
