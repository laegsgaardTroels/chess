import numpy as np
import logging

logger = logging.getLogger(__name__)


class BaseAgent:
    """A Base class for agents."""

    def __init__(self, color='black'):
        self.color = color

    def policy(self, game):
        raise NotImplementedError("Should be implemented in subclass.")


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
            # logger.info(
            #     f"{' -> '.join(chess_notation(move))}. value: {value}.\n"
            # )
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
