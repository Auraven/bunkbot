from discord import Message, Embed
from discord.ext.commands import command, Context

from ...bunkbot import BunkBot
from ...cogs.youtube.youtube_result import YoutubeResult
from ...services.channel_service import ChannelService
from ...services.registry import CHANNEL_SERVICE
from ...util.functions import get_cmd_params

YOUTUBE_DESCRIPTION = """
    Search for a youtube video with a given query. Display related videos with !more and re-link a related video with !ytl

    Example: !yt heroes of the storm
    Example: !more
    Example: !ytl 2
"""

MORE_TITLE = "Type !ytl 1-5 to link another video\nType !link or !link 0 to relink the original result\n"

class Youtube:
    def __init__(self, bot: BunkBot, channels: ChannelService):
        self.bot: BunkBot = bot
        self.message: Message = None
        self.channels: ChannelService = channels
        self.yt_result: YoutubeResult = YoutubeResult()
        self.yt_link: str = ""


    # perform a basic youtube search with a given
    # keyword - use beautiful soup to scrape HTML and return the result
    @command(pass_context=True, help=YOUTUBE_DESCRIPTION, aliases=["youtube"])
    async def yt(self, ctx: Context) -> None:
        try:
            params: list = get_cmd_params(ctx)

            if len(params) == 0:
                await self.bot.say("No youtube query given")
                return

            await self.channels.start_typing(ctx)

            self.yt_link = self.yt_result.query(params)

            self.message = await self.bot.say(self.yt_link)
        except Exception as e:
            await self.bot.handle_error(e, "yt")


    # replace the video from the previous search based
    # on the value entered (1-5)
    @command(pass_context=True, help="Link another youtube result from the last search", aliases=["ytl"])
    async def link(self, ctx: Context) -> None:
        try:
            params = get_cmd_params(ctx)

            if len(params) < 1 or not params[0].isdigit() or int(params[0]) > len(self.yt_result.ids):
                await self.bot.say("Please enter a valid video number from 0 to 5")
                return

            self.yt_link = await self.bot.edit_message(self.message, self.yt_result.get_link(int(params[0])))
            await self.bot.delete_message(ctx.message)
        except Exception as e:
            await self.bot.handle_error(e, "ytl")


    # get a list of related videos from the last
    #youtube search
    @command(pass_context=True, help="Get a list of related videos from the last youtube search")
    async def more(self, ctx) -> None:
        e_title = "Type !ytl 1-5 to link another video\nType !ytl or !ytl 0 to relink the original result\n"
        e_message = "\n".join(self.yt_result.titles)
        embed = Embed(title=e_title, description=e_message, color=int("CC181E", 16))

        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)


def setup(bot: BunkBot) -> None:
    bot.add_cog(Youtube(bot, CHANNEL_SERVICE))
