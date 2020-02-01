import json

from chess import Game
from chess import Agent


def test_policy():
    """Test the agent in naive examples."""
    agent = Agent(color='black')
    game = Game(current_color='white')
    game.move((7, 1), (1, 1))
    move = agent.policy(game)
    assert move == ((0, 2), (1, 1)), (
        f"Agent should take horse with bishop.But it's policy is {move}, with "
        f"actions values:\n{str(agent)}\n{game}"
    )
