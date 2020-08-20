from chess.board import Board
from chess.agent import RandomAgent
from chess.pieces import Empty

import copy
import logging

logger = logging.getLogger(__name__)


class Game:

    def __init__(
        self,
        board=None,
        white_player=RandomAgent,
        black_player=RandomAgent,
        current_color='white',
    ):
        self.white_player = white_player(color='white')
        self.black_player = black_player(color='black')
        self.current_color = current_color
        if board is None:
            self.board = Board()
        else:
            self.board = Board(board)

    def __str__(self):
        return str(self.board)

    def moves(self, color, with_piece=False):
        """Generate moves for a given color.

        NB: Important that this is a generator for lazy evaluation.
        """
        for row in self.board:
            for piece in row:
                if piece.color == color and piece.moves():
                    from_ = piece.position
                    for to in piece.moves():
                        if with_piece:
                            yield piece, (from_, to)
                        else:
                            yield (from_, to)

    def moves_str(self, color):
        moves_strs = []
        for piece, move in self.moves(color, with_piece=True):
            move_str = Board.chess_move_notation(move)
            moves_strs.append(
                f"{str(piece)} : {move_str}"
            )
        return '\n'.join(moves_strs)

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

    def is_check(self, color):
        king = self.board.get_king(color)
        opponent_check_pieces = []
        for piece, move in self.moves(
            self.opponent_color(color),
            with_piece=True,
        ):
            from_, to = move
            if king.position == to:
                opponent_check_pieces.append(
                    piece
                )
        return opponent_check_pieces

    def is_draw(self):
        pieces_left = []
        for row in self.board:
            for piece in row:
                if not isinstance(piece, Empty):
                    pieces_left.append(piece)
        if len(pieces_left) == 2:
            return True
        return False

    def is_checkmate(self, color):
        for move in self.moves(color):
            new_game = self.simulate_move(*move)
            if not new_game.is_check(color):
                return False
        return True

    def opponent_color(self, color=None):
        from_to = {'white': 'black', 'black': 'white'}
        if color is None:
            return from_to[self.current_color]
        else:
            return from_to[color]

    def play(self, verbose=False):
        """The game loop.
        """
        if verbose:
            print(r"""
            (  ____ \|\     /|(  ____ \(  ____ \(  ____ \
            | (    \/| )   ( || (    \/| (    \/| (    \/
            | |      | (___) || (__    | (_____ | (
            | |      |  ___  ||  __)   (_____  )(_____  )
            | |      | (   ) || (            ) |      ) |
            | (____/\| )   ( || (____/\/\____) |/\____) |
            (_______/|/     \|(_______/\_______)\_______)

            """)
            print(f"White player: {self.white_player}")
            print(f"Black player: {self.black_player}")
            print()
            print()
        try:
            while not (
                self.is_checkmate(self.current_color)
                or self.is_draw()
            ):
                if verbose:
                    print(self)
                    print()

                move = self.get_move()
                if move is None:
                    print()
                    print("Invalid move...\n")
                    continue
                print()
                print('moving', chess_move_notation(move))
                print()
                from_, to = move
                new_game = self.simulate_move(from_, to)
                if new_game.is_check(self.current_color):
                    if verbose:
                        print()
                        print("Cannot move into check...\n")
                    continue
                self.move(from_, to)

                # TODO: Below looks like shit
                check = self.is_check(self.current_color)
                if check:
                    if verbose:
                        check_str = '\n'.join(map(str, check))
                        print()
                        print(f'{self.current_color} is check by {check_str}')
                        print()

            if verbose:
                if self.is_draw():
                    self.winner = None
                    print()
                    print()
                    print("It is a draw!")
                    logger.info("it is a draw.")
                else:
                    self.winner = self.opponent_color()
                    print()
                    print()
                    print(f"Winner is {self.winner}")
                    print(f"White player: {self.white_player}")
                    print(f"Black player: {self.black_player}")
                    logger.info(f"winner is {self.winner}.")

            if verbose:
                print()
                print()
                print("White Moves:")
                print(self.moves_str('white'))
                print("Black Moves:")
                print(self.moves_str('black'))
                print()

        except KeyboardInterrupt:
            if verbose:
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
