import pytest

from chess import Game
from random import choice

SIMULATIONS = 10


@pytest.mark.parametrize("idx", range(SIMULATIONS))
def test_simulation(idx):
    """Test that a randomly simulated game doesn't fail."""
    game = Game()
    while not (
       game.board.get_king(game.current_color) is None
       or game.is_checkmate(game.current_color)
       or game.is_draw()
    ):
        move = choice(list(game.moves(game.current_color)))
        game.move(*move)
