import json
import numpy as np

class Agent:

    def __init__(self, color='black'):
        self.color = color
        self.depth = 4
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
            value = self.alphabeta(root_node, self.depth - 1, False)
            if value >= max_value:
                best_move = move
                max_value = value

            # Save for debugging.
            self.last_action_value[str(move)] = str(value)

        return best_move

    def alphabeta(
            self,
            node, depth,
            alpha=-np.inf, beta=np.inf, maximizing_player=True
        ):
        moves = node.moves(node.current_color)
        if depth == 0 or len(moves) == 0:
            return self.state_value(node)
        if maximizing_player:
            value = - np.inf
            for move in moves:
                new_node = node.simulate_move(*move)
                value = max(value, self.alphabeta(new_node, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = np.inf
            for move in moves:
                new_node = node.simulate_move(*move)
                value = min(value, self.alphabeta(new_node, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
