from chess.board import Board

from chess.pieces import Empty

import copy
import logging

logger = logging.getLogger(__name__)


class Game:

    def __init__(
        self,
        black_player,
        white_player,
        current_color='white',
        board=None,
    ):
        self.black_player = black_player(color='black')
        self.white_player = white_player(color='white')
        self.current_color = current_color
        if board is None:
            self.board = Board()
        else:
            self.board = Board(board)

    def __str__(self):
        return str(self.board)

    def moves(self, color):
        """Generate moves for a given color.

        NB: Important that this is a generator for lazy evaluation.
        """
        for row in self.board:
            for piece in row:
                if piece.color == color and piece.moves():
                    from_ = piece.position
                    for to in piece.moves():
                        yield (from_, to)

    def copy(self):
        return copy.deepcopy(self)

    def move(self, from_, to):
        self.board[to] = self.board[from_]
        self.board[from_] = Empty(None, self)
        self.current_color = self.opponent_color()
        return self

    def simulate_move(self, from_, to):
        new_game = self.copy()
        return new_game.move(from_, to)

    def is_checkmate(self, color):
        return (
            self.is_check(color)
            & self.cant_move_out_of_check(color)
        )

    def is_check(self, color):
        king = self.board.get_king(color)
        enemy_moves = [
            to for from_, to in self.moves(self.opponent_color(color))
        ]
        return king.position in enemy_moves

    def is_draw(self):
        pieces_left = []
        for row in self.board:
            for piece in row:
                if not isinstance(piece, Empty):
                    pieces_left.append(piece)
        if len(pieces_left) == 2:
            return True
        return False

    def cant_move_out_of_check(self, color):
        for move in self.moves(color):
            new_board = self.simulate_move(*move)
            if not new_board.is_check(color):
                return False
        return True

    def opponent_color(self, color=None):
        from_to = {'white': 'black', 'black': 'white'}
        if color is None:
            return from_to[self.current_color]
        else:
            return from_to[color]

    def play(self):
        """Used to run the game.
        """
        try:
            while not (
                self.board.get_king(self.current_color) is None
                or self.is_checkmate(self.current_color)
                or self.is_draw()
            ):
                print(self)
                print()
                print()

                move = self.get_move()
                if move is None:
                    continue

                from_, to = move
                self.move(from_, to)

                if self.is_checkmate(self.current_color):
                    print(f'{self.current_color} is check')
                    print()

            print()
            print()
            print(f"Winner is {self.opponent_color()}")
            logger.info(f"winner is {self.opponent_color()}.")

        except KeyboardInterrupt:
            print()
            print()
            print("Game stopped.")
            logger.info("game stopped due to keyboard interrupt.")

    def get_move(self):
        """Get the move from the agent or the player.
        """
        if self.current_color == 'black':
            return self.black_player.policy(self)
        else:
            return self.white_player.policy(self)
