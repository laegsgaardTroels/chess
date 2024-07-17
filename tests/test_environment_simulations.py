import pytest

from chess._agent import (
    RandomAgent,
    simulate,
)
from chess._constants import (
    EMPTY,
    MAX_PLY,
)


n_simulations = 50


@pytest.mark.parametrize("seed", list(range(n_simulations)))
def test_environment_simulate_random_game(seed):
    state_log, _ = simulate(
        white_player=RandomAgent(seed=seed),
        black_player=RandomAgent(seed=seed),
        verbose=True,
    )
    assert (
        state_log[-1]["is_black_checkmate"]
        or state_log[-1]["is_white_checkmate"]
        or state_log[-1]["is_draw"]
    )
    assert state_log[-1]["ply"] <= MAX_PLY
    assert state_log[-1]["black_king"] != EMPTY
    assert state_log[-1]["white_king"] != EMPTY
