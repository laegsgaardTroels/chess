import numpy as np

from chess.pieces import Piece
from chess.pieces import Tower
from chess.pieces import Horse
from chess.pieces import Bishop
from chess.pieces import King
from chess.pieces import Queen
from chess.pieces import Pawn
from chess.pieces import Empty

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8]
SPACE = ' '


class Board:
    """The chess board.

    The board contains all the pieces and the pieces contains a reference to
    the board.
    """

    def __init__(self, board=None):
        if board is None:
            self.board = self._create_board()
        else:
            self.board = board

    def __deepcopy__(self, memo=None):
        new_board = []
        for i, row in enumerate(self.board):
            new_row = []
            for j, piece in enumerate(row):
                new_piece = piece.__class__(
                    color=piece.color,
                    board=new_board,
                    position=piece.position
                )

                new_row.append(new_piece)
            new_board.append(new_row)
        new_board = Board(board=new_board)
        return new_board

    @property
    def board(self):
        """Is the board of the correct type etc."""
        return self._board

    @board.setter
    def board(self, value):

        for i, row in enumerate(value):
            for j, piece in enumerate(row):
                piece.board = self
                piece.position = (i, j)

        if isinstance(value, list):
            value = np.array(value)

        # Run checks
        if not isinstance(value, np.ndarray):
            raise ValueError('Board should be a numpy array.')

        self._board = value

    def __getitem__(self, position):
        i, j = position
        if 0 <= i < 8 and 0 <= j < 8:
            return self.board[position]
        return None

    def __setitem__(self, position, piece):
        self.board[position] = piece
        piece.board = self
        piece.position = position

    def __len__(self):
        return 8

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.board == other
        elif isinstance(other, Board):
            return np.all(self.board == other.board)
        return False

    def __iter__(self):
        return self.board.__iter__()

    def __str__(self):
        lines = []
        lines.append(
            ' '
            + SPACE
            + SPACE.join(LETTERS)
            + SPACE
            + ' '
        )
        for idx, row in enumerate(self):
            lines.append(
                str(8 - idx)
                + SPACE
                + SPACE.join(map(str, row))
                + SPACE
                + str(8 - idx)
            )
        lines.append(
            ' '
            + SPACE
            + SPACE.join(LETTERS)
            + SPACE
            + ' '
        )
        return '\n'.join(lines)

    def copy(self):
        return self.__deepcopy__(None)

    def _create_board(self):
        """Create a chess board."""
        return np.array([
            self.back_row('black'),
            self.pawn_row('black'),
        ] + [
            self.empty_row() for i in range(4)
        ] + [
            self.pawn_row('white'),
            self.back_row('white'),
        ])

    def back_row(self, color):
        return [
            Tower(color, self),
            Horse(color, self),
            Bishop(color, self),
            King(color, self),
            Queen(color, self),
            Bishop(color, self),
            Horse(color, self),
            Tower(color, self),
        ]

    def pawn_row(self, color):
        return [Pawn(color, self) for j in range(len(self))]

    def empty_row(self):
        return [Empty(None, self) for j in range(len(self))]

    def get_king(self, color):
        """Returns None if no king is found."""
        for row in self.board:
            for piece in row:
                if (piece.color == color) & isinstance(piece, King):
                    return piece
        return None

    @staticmethod
    def chess_notation(move):
        from_, to = move
        int_to_letter = dict(zip(range(8), LETTERS))
        cn_from = f"{int_to_letter[from_[1]]}{8 - from_[0]}"
        cn_to = f"{int_to_letter[to[1]]}{8 - to[0]}"
        return cn_from, cn_to

    @staticmethod
    def translate(chess_notation):
        if len(chess_notation) != 2:
            return None
        letter, number = chess_notation
        number = int(number)
        if not (letter in LETTERS and number in NUMBERS):
            return None
        i = 8 - number
        j = dict(zip(LETTERS, range(8)))[letter]
        return i, j

    @staticmethod
    def chess_move_notation(move):
        return '->'.join(Board.chess_notation(move))
