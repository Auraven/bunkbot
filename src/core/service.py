from discord import Guild

from ..bunkbot import BunkBot
from ..channel.log_service import LogService
from ..db.database_service import DatabaseService
from ..etc.config_service import ConfigService

class Service:
    """
    Base class which all services should extend - this will
    hold base information for BunkBot - server ref, database ref, etc

    Parameters
    -----------
    bot: BunkBot
        Instance of the bot which all extended classes can utilize

    databse: DatabaseService (optional)
        Optional instance of the database service (usually injected unless its the db service itself)
    """
    def __init__(self, bot: BunkBot, database: DatabaseService = None):
        self.database: DatabaseService = database
        self.config: ConfigService = ConfigService()
        self.logger: LogService = LogService()
        self.bot: BunkBot = bot
        self.server: Guild = None
        bot.on_initialized += self.load

    # When bunkbot is loaded, all services
    # will load the server instance and other
    # default utils
    async def load(self) -> None:
        if self.bot.server:
            self.server = self.bot.server
            