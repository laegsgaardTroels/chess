from chess.agent import BaseAgent
from chess.board import Board

import numpy as np
import logging
import json

logger = logging.getLogger(__name__)


class AlphaBetaAgent(BaseAgent):
    """Agent using minimax with alpha-beta pruning."""

    def __init__(self, color='black', depth=3):
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
        best_moves = []
        for move in game.moves(self.color):
            root_node = game.simulate_move(*move)
            value = self.alphabeta(
                node=root_node,
                depth=self.depth - 1,
                maximizing_player=False
            )
            if value == max_value:
                best_moves.append(move)
            if value > max_value:
                best_moves = [move]
                max_value = value

            # TODO: Make below nicer.
            last_action_value[Board.chess_move_notation(move)] = value
        logger.info(json.dumps(last_action_value))
        return sorted(best_moves, key=distance_to_board_center)[0]

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


def distance_to_board_center(move):
    from_, to = move
    return (
        (to[0] - 3.5) ** 2
        + (to[1] - 3.5) ** 2
    )
