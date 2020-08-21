class BaseAgent:
    """A Base class for agents."""

    def __init__(self, color='black'):
        self.color = color

    def policy(self, game):
        raise NotImplementedError("Should be implemented in subclass.")
