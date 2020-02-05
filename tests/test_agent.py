import json

from chess import Game
from chess import Agent


def test_policy():
    """How does the agent handle naive examples."""
    agent = Agent(color='black', depth=2)
    game = Game(current_color='white')
    game.move((7, 1), (1, 1))
    move = agent.policy(game)
    assert move == ((0, 2), (1, 1)), (
        f"Agent should take horse with bishop.But it's policy is {move}, with "
        f"actions values:\n{str(agent)}\n{game}"
    )


def test_alphabeta():
    """Does the alpha-beta search work as expected."""
    agent = Agent(color='black', depth=2)
    game = Game(current_color='white')
    game.move((7, 0), (0, 0))
    _ = agent.policy(game)
    values = list(agent.last_action_value.values())
    assert all(float(value) < 0 for value in values), (
        f"The values should all be negative"
        f"actions values:\n{str(agent)}\n{game}"
    )
