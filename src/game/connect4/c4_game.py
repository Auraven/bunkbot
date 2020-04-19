from discord import TextChannel, Message

from .c4_constants import PLAYER1_PIECE, PLAYER2_PIECE
from .c4_board import ConnectFourBoard
from .c4_renderer import ConnectFourRenderer
from ..custom_game import CustomGame
from ...core.bunk_user import BunkUser


"""
Instance of a game itself - connected to
a creator and parent channel similar to hangman
"""
class ConnectFourGame(CustomGame):
    def __init__(self, creator: BunkUser, channel: TextChannel):
        super().__init__(channel)
        self.creator: BunkUser = creator
        self.opponent: BunkUser = None
        self.board: ConnectFourBoard = None
        self.renderer: ConnectFourRenderer = ConnectFourRenderer(channel)


    # start a new game and render a new grid
    # into the channel using the renderer
    async def start(self) -> None:
        self.board = ConnectFourBoard()
        await self.renderer.create_game(self.board, self.creator)


    async def update(self, message: Message, user: BunkUser) -> None:
        if not await self.is_cancel(message, self.creator):
            player_id: int = message.author.id
            piece: str = PLAYER1_PIECE if player_id == self.creator.id else PLAYER2_PIECE
            content: str = self.get_content(message)
            is_bad_option: bool = len(content) > 1 or not content.isdigit() or int(content) > 7

            if not is_bad_option:
                self.board.update_piece(int(content)-1, player_id, piece)
                await self.renderer.update_board(self.board, False, user)
