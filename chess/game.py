from chess import config

from chess.board import Board
from chess.agent import RandomAgent
from chess.pieces import Empty
from chess.pieces import Queen
from chess.pieces import Pawn

import copy
import logging

logger = logging.getLogger(__name__)


class Game:
    """The Game has the game loop and specific rules like check, promotion and castling.

    The game contains the agents playing and the board. A game can simulate moves, this
    can be used by the agents.
    """

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

    def copy(self):
        return copy.deepcopy(self)

    def move(self, from_, to):
        piece = self.board[from_]

        # If a Pawn reaches eigth rank then replace by a queen.
        if isinstance(piece, Pawn) and to[0] in [0, 7]:
            piece = Queen(self.current_color)

        self.board[to] = piece
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

    def is_draw(self, game_history):
        pieces_left = []
        for row in self.board:
            for piece in row:
                if not isinstance(piece, Empty):
                    pieces_left.append(piece)
        if len(pieces_left) == 2:
            return True

        # Threefold repetition rule.
        if config.THREEFOLD_REPETITION_RULE:
            if sum(
                str(self) == board
                for board in game_history
            ) >= 3:
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
        try:
            game_history = []
            if verbose:
                print(self)
                print()
            while not (
                self.is_checkmate(self.current_color)
                or self.is_draw(game_history)
            ):
                move = self.get_move()
                if move is None:
                    print("Invalid move...\n")
                    print()
                    continue
                game_history.append(str(self))
                self.move(*move)
                if verbose:
                    print('Color:', self.opponent_color())
                    print('Move:', Board.chess_move_notation(move))
                    print()
                    print(self)
                    print()

            if verbose:
                if self.is_draw(game_history):
                    self.winner = None
                    print("It is a draw!")
                    logger.info("it is a draw.")
                else:
                    self.winner = self.opponent_color()
                    print(f"Winner is {self.winner}")
                    print(f"White player: {self.white_player}")
                    print(f"Black player: {self.black_player}")
                    logger.info(f"winner is {self.winner}.")

        except KeyboardInterrupt:
            if verbose:
                print("Game stopped.")
            logger.info("game stopped due to keyboard interrupt.")

    def get_move(self):
        """Get the move from the agent or the player.
        """
        if self.current_color == 'black':
            return self.black_player.policy(self)
        else:
            return self.white_player.policy(self)
