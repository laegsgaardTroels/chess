import numpy as np
import logging

import json

from chess.pieces import Empty
from chess.utils import chess_notation

logger = logging.getLogger(__name__)


class BaseAgent:
    """A Base class for agents."""

    def __init__(self, color='black'):
        self.color = color

    def policy(self, game):
        raise NotImplementedError("Should be implemented in subclass.")


class HumanAgent(BaseAgent):
    """A human agent."""

    def translate(self, chess_notation):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        if len(chess_notation) != 2:
            return None
        letter, number = chess_notation
        number = int(number)
        if not (letter in letters and number in numbers):
            return None
        i = 8 - number
        j = dict(zip(letters, range(8)))[letter]
        return i, j

    def policy(self, game):
        str_from = input('Move from: ')
        str_to = input('Move to: ')
        print()
        from_ = self.translate(str_from)
        to = self.translate(str_to)

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
            print("Can move this piece to here...\n")
            return None
        if game.board[from_].color != self.color:
            print('Not this players turn...\n')
            return None
        return from_, to


class AlphaBetaAgent(BaseAgent):
    """Agent using minimax with alpha-beta pruning."""

    def __init__(self, color='black', depth=2):
        super().__init__(color)
        self.depth = depth
        self.piece_value = {
            'Empty': 0,
            'Pawn': 1,
            'Horse': 3,
            'Bishop': 3,
            'Tower': 5,
            'Queen': 9,
            'King': 1e6,
        }

    def state_value(self, game):
        value = 0
        for row in game.board:
            for piece in row:
                piece_value = self.piece_value[type(piece).__name__]
                if piece.color == self.color:
                    value += piece_value
                else:
                    value -= piece_value
        return value

    def policy(self, game):
        max_value = - np.inf
        last_action_value = {}
        for move in game.moves(self.color):
            root_node = game.simulate_move(*move)
            value = self.alphabeta(
                node=root_node,
                depth=self.depth - 1,
                maximizing_player=False
            )
            if value >= max_value:
                best_move = move
                max_value = value

            # TODO: Make below nicer.
            last_action_value['->'.join(chess_notation(move))] = value
        logger.info(json.dumps(last_action_value))
        return best_move

    def alphabeta(
        self,
        node, depth,
        alpha=-np.inf, beta=np.inf,
        maximizing_player=True,
    ):
        """Minimax with alpha-beta pruning.

        A lot is stolen from the pseudocode in [1].

        References:
            [1] https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Heuristic_improvements
        """

        if depth == 0:
            value = self.state_value(node)
        else:
            if maximizing_player:
                value = - np.inf
                for move in node.moves(node.current_color):
                    new_node = node.simulate_move(*move)
                    new_value = self.alphabeta(new_node, depth - 1, alpha, beta, False)
                    value = max(value, new_value)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            else:
                value = np.inf
                for move in node.moves(node.current_color):
                    new_node = node.simulate_move(*move)
                    new_value = self.alphabeta(new_node, depth - 1, alpha, beta, True)
                    value = min(value, new_value)
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
        return value
