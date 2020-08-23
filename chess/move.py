from chess import config

from chess.pieces import Queen
from chess.pieces import Pawn
from chess.pieces import Empty


class BaseMove:
    def __call__(self, game):
        raise NotImplementedError("Should be implemented in subclass.")


class Move(BaseMove):

    def __init__(self, piece, from_, to):
        self.piece = piece
        self.from_ = from_
        self.to = to

    def __eq__(self, other):
        if (
            self.piece == other.piece
            and self.from_ == other.from_
            and self.to == self.to
        ):
            return True
        return False

    def __call__(self, game):
        piece = game.board[self.from_]

        # If a Pawn reaches eigth rank then replace by a queen.
        if isinstance(piece, Pawn) and self.to[0] in [0, 7]:
            piece = Queen(game.current_color)

        game.board[self.to] = piece
        game.board[self.from_] = Empty(None, self)
        game.current_color = game.opponent_color()
        return game

    def __str__(self):
        int_to_letter = dict(zip(range(8), config.LETTERS))
        cn_from = f"{int_to_letter[self.from_[1]]}{8 - self.from_[0]}"
        cn_to = f"{int_to_letter[self.to[1]]}{8 - self.to[0]}"
        return f'{cn_from} -> {cn_to}'


class Castling(BaseMove):
    pass
