import pytest
from chess._constants import WHITE, BLACK
from chess._utils import (
    state_init,
    state_str,
    board_flipud,
    board_swapcolor,
)


is_white_checkmate_testdata = [
    (
        "♜♞♝♛♚♝♞♜"  # Starting position
        "♟♟♟♟♟♟♟♟"
        "        "
        "        "
        "        "
        "        "
        "♙♙♙♙♙♙♙♙"
        "♖♘♗♕♔♗♘♖",
        False,
    ),
    (
        "♜♞♝ ♚♝♞♜"  # Checkmate: Fool's mate
        "♟♟♟♟ ♟♟♟"
        "        "
        "    ♟   "
        "      ♙♛"
        "     ♙  "
        "♙♙♙♙♙  ♙"
        "♖♘♗♕♔♗♘♖",
        True,
    ),
    (
        "        "  # Checkmate: Support mate
        "        "
        "♔♛♚     "
        "        "
        "        "
        "        "
        "        "
        "        ",
        True,
    ),
    (
        "        "  # Checkmate: Right triangle mate
        "        "
        "     ♚ ♔"
        "        "
        "        "
        "        "
        "        "
        "       ♛",
        True,
    ),
    (
        "        "  # Anderssen's mate
        "        "
        "        "
        "        "
        "        "
        "     ♚  "
        "      ♟ "
        "      ♔♜",
        True,
    ),
]
is_black_checkmate_testdata = [
    (board_swapcolor(board_flipud(board)), expected_is_white_check)
    for board, expected_is_white_check in is_white_checkmate_testdata
]


@pytest.mark.parametrize("board,expected_is_white_check", is_white_checkmate_testdata)
def test_is_white_check(env, board, expected_is_white_check):
    state = state_init(color=WHITE, board=board)
    actual_is_white_check = env.is_white_check(state)
    assert (
        actual_is_white_check == expected_is_white_check
    ), f"\n{state_str(state)}\n{actual_is_white_check=}\n{expected_is_white_check=}"


@pytest.mark.parametrize("board,expected_is_black_check", is_black_checkmate_testdata)
def test_is_black_check(env, board, expected_is_black_check):
    state = state_init(color=BLACK, board=board)
    actual_is_black_check = env.is_black_check(state)
    assert (
        actual_is_black_check == expected_is_black_check
    ), f"\n{state_str(state)}\n{actual_is_black_check=}\n{expected_is_black_check=}"


@pytest.mark.parametrize("board,expected_is_white_checkmate", is_white_checkmate_testdata)
def test_is_white_checkmate(env, board, expected_is_white_checkmate):
    state = state_init(color=WHITE, board=board)
    actual_is_white_checkmate = env.is_white_checkmate(state)
    assert (
        actual_is_white_checkmate == expected_is_white_checkmate
    ), f"\n{state_str(state)}\n{actual_is_white_checkmate=}\n{expected_is_white_checkmate=}"


@pytest.mark.parametrize("board,expected_is_black_checkmate", is_black_checkmate_testdata)
def test_is_black_checkmate(env, board, expected_is_black_checkmate):
    state = state_init(color=BLACK, board=board)
    actual_is_black_checkmate = env.is_black_checkmate(state)
    assert (
        actual_is_black_checkmate == expected_is_black_checkmate
    ), f"\n{state_str(state)}\n{actual_is_black_checkmate=}\n{expected_is_black_checkmate=}"
