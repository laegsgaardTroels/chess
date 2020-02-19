import pytest

from chess import Game
from random import choice

SIMULATIONS = 10


@pytest.mark.parametrize("idx", range(SIMULATIONS))
def test_simulation(idx):
    """Test that a randomly simulated game doesn't fail."""
    game = Game()
    while not (
        game.is_checkmate(game.current_color)
        or game.is_draw()
        or game.is_check(game.opponent_color(game.current_color))
    ):
        move = choice(game.moves(game.current_color))
        game.move(*move)
