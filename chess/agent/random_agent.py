from chess.agent import BaseAgent

import random


class RandomAgent(BaseAgent):
    """A Base class for agents."""

    def policy(self, game):
        moves = list(game.moves(self.color))
        return random.choice(moves)
