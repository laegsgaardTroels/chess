from chess.board import Board
from chess.agent import RandomAgent
from chess.pieces import Empty
from chess.move import Move

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

        self._game_history = []

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
                        new_move = Move(piece, from_, to)
                        yield new_move

    def copy(self):
        return copy.deepcopy(self)

    def simulate(self, move):
        new_game = self.copy()
        return move(new_game)

    def is_check(self, color):
        check_moves = []
        for move in self.moves(self.opponent_color(color)):
            if (
                self
                .simulate(move)
                .board
                .get_king(color)
            ) is None:
                check_moves.append(
                    move
                )
        return check_moves

    def is_draw(self):
        pieces_left = []
        for row in self.board:
            for piece in row:
                if not isinstance(piece, Empty):
                    pieces_left.append(piece)
        if len(pieces_left) == 2:
            return True

        # Threefold repetition rule.
        if sum(
            str(self) == board
            for board in self._game_history
        ) >= 3:
            return True
        return False

    def is_checkmate(self, color):
        for move in self.moves(color):
            new_game = self.simulate(move)
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

            if verbose:
                print(self)
                print()

            while not (
                self.is_checkmate(self.current_color)
                or self.is_draw()
            ):

                move = self.get_move()
                if move is None:
                    print("Invalid move...\n")
                    print()
                    continue
                self._game_history.append(str(self))
                move(self)

                if verbose:
                    print(f'Color: {self.opponent_color()}')
                    print(f'Move: {move}')
                    print()
                    print(self)
                    print()

            if verbose:
                if self.is_draw():
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
