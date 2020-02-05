from chess.utils import chess_notation

import json
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Agent:

    def __init__(self, color='black', depth=4):
        self.color = color
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
        self.last_action_value = {}

    def __str__(self):
        return json.dumps(self.last_action_value, indent=4)

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

            # Save for debugging.
            self.last_action_value[' -> '.join(chess_notation(move))] = value
            logger.debug(f"{' -> '.join(chess_notation(move))}. value: {value}.\n")
        logger.info(f"\n\n{self.__str__()}\n")
        return best_move

    def alphabeta(
            self,
            node, depth,
            alpha=-np.inf, beta=np.inf, maximizing_player=True,
            str_log=None,
        ):

        # Used for logging in root node.
        str_log = self.combine(str_log, str(node))

        # The algorithm.
        moves = node.moves(node.current_color)
        if depth == 0 or len(moves) == 0:
            value = self.state_value(node)
            logger.debug(f"\n\nstate value: {value}.\n{str_log}\n")
        elif maximizing_player:
            value = - np.inf
            for move in moves:
                new_node = node.simulate_move(*move)
                value = max(value, self.alphabeta(new_node, depth - 1, alpha, beta, False, str_log))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = np.inf
            for move in moves:
                new_node = node.simulate_move(*move)
                value = min(value, self.alphabeta(new_node, depth - 1, alpha, beta, True, str_log))
                beta = min(beta, value)
                if alpha >= beta:
                    break

        return value

    def combine(self, old_log, new_log):
        if old_log is None:
            return new_log
        return '\n'.join(map(
            lambda old_new: '    '.join(old_new),
            zip(old_log.splitlines(), new_log.splitlines())
        ))
