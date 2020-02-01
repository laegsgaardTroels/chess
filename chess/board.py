import numpy as np
import copy

from chess.pieces import *


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
            return all(self.board == other.board)
        return False

    def __iter__(self):
        return self.board.__iter__()

    def __str__(self):
        lines = []
        for idx, row in enumerate(self):
            lines.append(str(8 - idx) + ' ' + ' '.join(map(str, row)))
        lines.append('  a b c d e f g h')
        return '\n'.join(lines)

    def copy(self):
        return Board(copy.deepcopy(self.board))

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
        for row in self.board:
            for piece in row:
                if (piece.color == color) & isinstance(piece, King):
                    return piece
        raise ValueError(f'Missing king of color {color}')
