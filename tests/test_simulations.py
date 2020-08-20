import pytest

from chess.game import Game
from chess.agent import RandomAgent

SIMULATIONS = 5


@pytest.mark.parametrize("idx", range(SIMULATIONS))
def test_simulation(idx):
    """Test that a randomly simulated game doesn't fail."""
    game = Game(
        white_player=RandomAgent,
        black_player=RandomAgent,
    )
    try:
        game.play()
    except Exception as exception:
        print(game.board)
        raise exception
