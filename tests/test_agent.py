from chess.game import Game
from chess.agent import AlphaBetaAgent


def test_alpha_beta_agent_policy():
    """How does the agent handle naive examples."""
    agent = AlphaBetaAgent(color='black', depth=2)
    game = Game(current_color='white')
    game.move((7, 1), (1, 1))
    move = agent.policy(game)
    assert move == ((0, 2), (1, 1)), (
        f"Agent should take horse with bishop. But it's policy is {move}, "
        f"with actions values:\n{str(agent)}\n{game}"
    )
