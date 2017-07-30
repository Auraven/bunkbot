"""
Roll a random number
"""
from discord import Embed
from random import randint
from discord.ext import commands
from ..bunkbot import BunkBot

DESCRIPTION = """Roll a random value between 0 and 100.  Optionally, you may pass a value range.\n
    Example: !roll
    Example: !roll 1-10
"""

class Roll:
    def __init__(self, bot: BunkBot):
        self.bot = bot

    # roll a random number
    # optionally specify a value range with default 0-100
    @commands.command(pass_context=True, cls=None, help=DESCRIPTION)
    async def roll(self, ctx: commands.Context) -> None:
        try:
            self.bot.send_typing(ctx.message.channel)

            min_val = 0
            max_val = 100
            params = self.bot.get_cmd_params(ctx)

            if len(params) > 0:
                if "-" in params[0]:
                    p_split = params[0].split("-")
                    if p_split[0].isdigit() and p_split[1].isdigit():
                        val_1 = int(p_split[0])
                        val_2 = int(p_split[1])
                        min_val = val_1 if val_1 <= val_2 else val_2
                        max_val = val_1 if val_2 <= val_1 else val_2

            title = "Rolling ({0}-{1})".format(min_val, max_val)
            message = "{0} rolls {1}".format(self.bot.get_author(ctx), str(randint(min_val, max_val)))

            await self.bot.say_embed(Embed(title=title, description=message))
        except Exception as e:
            await self.bot.handle_error(e, "roll")


def setup(bot) -> None:
    bot.add_cog(Roll(bot))