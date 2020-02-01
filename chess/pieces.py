import numpy as np


class Piece:
    """An abstract class for a piece on the board."""

    def __init__(self, color=None, board=None):
        self.color = color
        self.board = board

    @property
    def position(self):
        i, j = np.where(self.board == self)
        return int(i), int(j)

    @position.setter
    def position(self, value):
        self.board.move(
            from_=self.position,
            to=value
        )

    def move(self, value):
        self.board.move(
            from_=self.position,
            to=value
        )

    def is_opponent(self, other):
        """Return the color of the opponent."""
        if other.color is None:
            return False
        return self.color != other.color

    def moves(self):
        """Should return a list of all moves e.g. [(1,1), (1,2), ..]."""
        raise NotImplementedError()

    def __str__(self):
        """Return a string representation of the piece."""
        if self.color is None:
            return ' '
        return getattr(self, self.color)

    def print_moves(self):
        new_board = board.copy()
        for move in self.moves():
            new_board[move] = '.'


class Empty(Piece):

    """No piece on the position is represented by the empty piece."""
    def moves(self):
        return None


class King(Piece):

    white = u'♔'
    black = u'♚'

    def moves(self):
        moves = []
        i, j = self.position
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                new_position = (i + di, j + dj)
                if self.board[new_position] is None:
                    continue
                elif self.board[new_position].color == self.color:
                    continue
                moves.append(new_position)
        return moves


class Pawn(Piece):

    white = u'♙'
    black = u'♟'

    def moves(self):
        i, j = self.position
        moves = []
        moves.extend(self.forward_move(i, j))
        moves.extend(self.attacking_moves(i, j))
        return moves

    def forward_move(self, i, j):
        if self.color == 'black':
            moves = [(i + 1, j)]
            if i == 1:
                moves = [(i + 1, j), (i + 2, j)]

        elif self.color == 'white':
            moves = [(i - 1, j)]
            if i == 6:
                moves = [(i - 1, j), (i - 2, j)]

        else:
            raise ValueError(f"Invalid color {self.color}")

        if all(
            isinstance(self.board[new_position], Empty)
            for new_position in moves
        ):
            return moves

        return []

    def attacking_moves(self, i, j):
        if self.color == 'black':
            moves = [(i + 1, j - 1), (i + 1, j + 1)]
        elif self.color == 'white':
            moves = [(i - 1, j - 1), (i - 1, j + 1)]
        else:
            raise ValueError(f"Invalid color {self.color}")
        moves = filter(
            lambda new_position:
                self.board[new_position] and
                self.is_opponent(self.board[new_position]),
            moves
        )
        return moves


class Tower(Piece):

    white = u'♖'
    black = u'♜'

    def moves(self):
        i, j = self.position
        moves = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for step in range(1, len(self.board)):
                new_position = (i + step * di, j + step * dj)
                if self.board[new_position] is None:
                    break
                elif isinstance(self.board[new_position], Empty):
                    moves.append(new_position)
                elif self.board[new_position].color == self.color:
                    break
                elif self.board[new_position].color != self.color:
                    moves.append(new_position)
                    break

        return moves


class Bishop(Piece):

    white = u'♗'
    black = u'♝'

    def moves(self):
        i, j = self.position
        moves = []
        for di in [-1, 1]:
            for dj in [-1, 1]:
                for s in range(1, len(self.board)):
                    new_position = (i + s * di, j + s * dj)
                    if self.board[new_position] is None:
                        break
                    elif isinstance(self.board[new_position], Empty):
                        moves.append(new_position)
                    elif self.board[new_position].color == self.color:
                        break
                    elif self.board[new_position].color != self.color:
                        moves.append(new_position)
                        break
        return moves


class Horse(Piece):

    white = u'♘'
    black = u'♞'

    def moves(self):
        i, j = self.position
        moves = []
        for di, dj in [
            (-2, -1), (2, 1), (2, -1), (-2, 1),
            (-1, -2), (1, 2), (1, -2), (-1, 2),
        ]:
            new_position = (i + di, j + dj)
            if self.board[new_position] is None:
                continue
            elif isinstance(self.board[new_position], Empty):
                moves.append(new_position)
            elif self.board[new_position].color == self.color:
                continue
            elif self.board[new_position].color != self.color:
                moves.append(new_position)
        return moves


class Queen(Piece):

    white = u'♕'
    black = u'♛'

    def moves(self):
        i, j = self.position
        moves = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                for s in range(1, len(self.board)):
                    new_position = (i + s * di, j + s * dj)
                    if self.board[new_position] is None:
                        break
                    elif isinstance(self.board[new_position], Empty):
                        moves.append(new_position)
                    elif self.board[new_position].color == self.color:
                        break
                    elif self.board[new_position].color != self.color:
                        moves.append(new_position)
                        break
        return moves


UNCODE_STR_TO_PIECE = {
    u'♔': King('white'),
    u'♚': King('black'),
    u'♕': Queen('white'),
    u'♛': Queen('black'),
    u'♘': Horse('white'),
    u'♞': Horse('black'),
    u'♗': Bishop('white'),
    u'♝': Bishop('black'),
    u'♖': Tower('black'),
    u'♜': Tower('black'),
    u'♙': Pawn('white'),
    u'♟': Pawn('black'),
    u' ': Empty(),
}
