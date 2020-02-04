from chess.board import Board
from chess.agent import Agent
from chess.pieces import *
from chess.utils import chess_notation

import copy
import logging
from itertools import chain

logger = logging.getLogger(__name__)


class Game:

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(
        self,
        board=None,
        current_color='black',
    ):
        if board is None:
            self.board = Board()
        else:
            self.board = Board(board)
        self.current_color = current_color

    def __str__(self):
        return str(self.board)

    def translate(self, chess_notation):
        if len(chess_notation) != 2:
            return None
        letter, number = chess_notation
        number = int(number)
        if not (letter in Game.letters and number in Game.numbers):
            return None
        i = 8 - number
        j = dict(zip(Game.letters, range(8)))[letter]
        return i, j

    def moves(self, color):
        moves = []
        for row in self.board:
            for piece in row:
                if piece.color == color and piece.moves():
                    from_ = piece.position
                    moves.extend([
                        (from_, to) for to in piece.moves()
                    ])
        return moves

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

    def play(self, agent=None):
        while not (self.is_checkmate(self.current_color) or self.is_draw()):
            print(self)
            print()
            if self.current_color == 'black':
                from_, to = agent.policy(self)
            else:
                str_from = input('Move from: ')
                str_to = input('Move to: ')
                print()
                from_ = self.translate(str_from)
                to = self.translate(str_to)

                if from_ is None or to is None:
                    print("Invalid move...\n")
                    continue
                if isinstance(self.board[from_], Empty):
                    print("Not a piece...\n")
                    continue
                if self.board[from_] is None:
                    print("Not on the board...\n")
                    continue
                if to not in self.board[from_].moves():
                    print("Can move this piece to here...\n")
                    continue
                if self.board[from_].color != self.current_color:
                    print('Not this players turn...\n')
                    continue
            self.move(from_, to)
            logger.info(
                f"\n\n{self.opponent_color()} moved "
                f"{' -> '.join(chess_notation((from_, to)))}."
                f"\n\n{game}\n"
            )
        print()
        print(f"Winner is {self.opponent_color()}")
        logger.info(f"winner is {self.opponent_color()}.")


if __name__ == '__main__':
    logging.basicConfig(
        filename='game.log',
        filemode='w',
        level=logging.INFO
    )
    agent = Agent()
    game = Game()
    game.play(agent)
