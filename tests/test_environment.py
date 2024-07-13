import pytest
import numpy as np
from chess._constants import WHITE
from chess._utils import (
    state_init,
    state_str,
    all_invariants,
    flipud_invariant,
    simulate_random_game,
)

n_simulations = 10

king_testdata = all_invariants(
    [
        (
            WHITE,
            "♔       "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            3,
        ),
        (
            WHITE,
            "        "
            " ♔      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            8,
        ),
        (
            WHITE,
            "        "
            " ♔      "
            "   ♚    "
            "        "
            "        "
            "        "
            "        "
            "        ",
            6,
        ),
        (
            WHITE,
            "        "
            " ♔      "
            "        "
            "   ♞    "
            "        "
            "        "
            "        "
            "        ",
            6,
        ),
    ]
) + flipud_invariant(
    [
        (
            WHITE,
            "        "
            "        "
            " ♟      "
            "   ♔    "
            "        "
            "        "
            "        "
            "        ",
            7,
        ),
    ]
)

knight_testdata = all_invariants(
    [
        (
            WHITE,
            "♘       "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            2,
        ),
        (
            WHITE,
            "        "
            " ♘      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            4,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "   ♘    "
            "        "
            "        "
            "        "
            "        ",
            8,
        ),
    ]
)

rook_testdata = all_invariants(
    [
        (
            WHITE,
            "        "
            "        "
            "   ♘    "
            "   ♖    "
            "        "
            "        "
            "        "
            "        ",
            19,
        ),
        (
            WHITE,
            " ♖      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            14,
        ),
        (
            WHITE,
            "♖       "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            14,
        ),
        (
            WHITE,
            "        "
            " ♖      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            14,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "   ♖    "
            "        "
            "        "
            "        "
            "        ",
            14,
        ),
    ]
) + flipud_invariant(
    [
        (
            WHITE,
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "♖   ♔   ",
            16,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "    ♔  ♖",
            15,
        ),
    ]
)

bishop_testdata = all_invariants(
    [
        (
            WHITE,
            "        "
            "        "
            "   ♘    "
            "   ♗    "
            "        "
            "        "
            "        "
            "        ",
            21,
        ),
        (
            WHITE,
            " ♗      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            7,
        ),
        (
            WHITE,
            "♗       "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            7,
        ),
        (
            WHITE,
            "        "
            " ♗      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            9,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "   ♗    "
            "        "
            "        "
            "        "
            "        ",
            13,
        ),
    ]
)

queen_testdata = all_invariants(
    [
        (
            WHITE,
            "        "
            "        "
            "   ♘    "
            "   ♕    "
            "        "
            "        "
            "        "
            "        ",
            32,
        ),
        (
            WHITE,
            " ♕      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            21,
        ),
        (
            WHITE,
            "♕       "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            21,
        ),
        (
            WHITE,
            "        "
            " ♕      "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            23,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "   ♕    "
            "        "
            "        "
            "        "
            "        ",
            27,
        ),
    ]
)

pawn_testdata = flipud_invariant(
    [
        (
            WHITE,
            "        "
            "        "
            "        "
            "        "
            "        "
            "        "
            "♙♙♙♙♙♙♙♙"
            "        ",
            16,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "        "
            "        "
            "♙♙♙♙♙♙♙♙"
            "        "
            "        ",
            8,
        ),
        (
            WHITE,
            "        "
            "        "
            "        "
            "        "
            " ♟      "
            "♙       "
            "        "
            "        ",
            2,
        ),
        (
            WHITE,
            "        "
            "♙       "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            5,
        ),
        (
            WHITE,
            "       ♟"
            "      ♙ "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            10,
        ),
        (
            WHITE,
            "     ♟♟♟"
            "      ♙ "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            10,
        ),
        (
            WHITE,
            "     ♟ ♟"
            "      ♙ "
            "        "
            "        "
            "        "
            "        "
            "        "
            "        ",
            15,
        ),
    ]
)

testdata = (
    king_testdata
    + knight_testdata
    + rook_testdata
    + bishop_testdata
    + queen_testdata
    + pawn_testdata
)


@pytest.mark.parametrize("color,board,expected_n_actions", testdata)
def test_environment_n_actions(env, color, board, expected_n_actions):
    state = state_init(color=color, board=board)

    actual_n_actions = len(env.actions(state))
    assert (
        actual_n_actions == expected_n_actions
    ), f"\n{state_str(state)}\n{actual_n_actions=}\n{expected_n_actions=}"

    state = state_init(color=color, board=board)
    next_state = env.step(state, env.actions(state))
    assert (
        len(next_state) == expected_n_actions
    ), f"\n{state_str(state)}\n{actual_n_actions=}\n{expected_n_actions=}"


@pytest.mark.parametrize("seed", list(range(n_simulations)))
def test_environment_simulate_random_game(env, seed):
    np.random.seed(seed)
    simulate_random_game(env)
