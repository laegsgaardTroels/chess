import pytest
import numpy as np
from chess._environment import bb_to_ij

n_simulations = 10


def random_bb():
    return np.uint64(0 | (1 << np.random.choice(range(64))))


@pytest.mark.parametrize("seed", list(range(n_simulations)))
def test_rook_attackset(env, seed):
    np.random.seed(seed)
    bishop = random_bb()
    i, j = bb_to_ij(bishop)
    np.random.seed(n_simulations + seed)
    blocker_mask = random_bb()
    assert env.rook_attackset(bishop, blocker_mask) == env.rook_attackset_slow(
        i, j, blocker_mask
    )


@pytest.mark.parametrize("seed", list(range(n_simulations)))
def test_bishop_attackset(env, seed):
    np.random.seed(seed)
    bishop = random_bb()
    i, j = bb_to_ij(bishop)
    np.random.seed(n_simulations + seed)
    blocker_mask = random_bb()
    assert env.bishop_attackset(bishop, blocker_mask) == env.bishop_attackset_slow(
        i, j, blocker_mask
    )


def test_rook_table(env):
    assert len(env._rook_table_lookup) == 64
    for key in env._rook_table_lookup:
        assert len(set(env._rook_table_lookup[key].values())) > 1


def test_bishop_table(env):
    assert len(env._bishop_table_lookup) == 64
    for key in env._bishop_table_lookup:
        assert len(set(env._bishop_table_lookup[key].values())) > 1
