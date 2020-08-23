from chess.agent import BaseAgent
from chess.pieces import Empty
from chess.board import Board
from chess.move import Move


class HumanAgent(BaseAgent):
    """A human agent."""

    def policy(self, game):
        print()
        str_from = input(
            'Move from : ')
        str_to = input(
            'Move to   : '
        )
        print()
        from_ = Board.translate(str_from)
        to = Board.translate(str_to)

        if from_ is None or to is None:
            print("Invalid move...\n")
            return None
        if isinstance(game.board[from_], Empty):
            print("Not a piece...\n")
            return None
        if game.board[from_] is None:
            print("Not on the board...\n")
            return None
        if to not in list(game.board[from_].moves()):
            print("Can't move this piece to here...\n")
            return None
        if game.board[from_].color != self.color:
            print('Not this players turn...\n')
            return None

        return Move(game.board[from_], from_, to)
