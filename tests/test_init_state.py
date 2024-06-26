import numpy as np
from chess import _utils
from chess._constants import (
    EMPTY,
    BLACK_ROOK,
    BLACK_KNIGHT,
    BLACK_BISHOP,
    BLACK_QUEEN,
    BLACK_KING,
    BLACK_PAWN,
    WHITE_ROOK,
    WHITE_KNIGHT,
    WHITE_BISHOP,
    WHITE_QUEEN,
    WHITE_KING,
    WHITE_PAWN,
    WHITE,
)


def test_init_state():
    state = _utils.init_state(
        color=WHITE,
        board=(
            "♜♞♝♛♚♝♞♜"
            "♟♟♟♟♟♟♟♟"
            "        "
            "        "
            "        "
            "        "
            "♙♙♙♙♙♙♙♙"
            "♖♘♗♕♔♗♘♖"
        ),
    )
    actual_board = state["board"]
    expected_board = np.array(
        [
            [
                BLACK_ROOK,
                BLACK_KNIGHT,
                BLACK_BISHOP,
                BLACK_QUEEN,
                BLACK_KING,
                BLACK_BISHOP,
                BLACK_KNIGHT,
                BLACK_ROOK,
            ],
            [
                BLACK_PAWN,
                BLACK_PAWN,
                BLACK_PAWN,
                BLACK_PAWN,
                BLACK_PAWN,
                BLACK_PAWN,
                BLACK_PAWN,
                BLACK_PAWN,
            ],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [
                WHITE_PAWN,
                WHITE_PAWN,
                WHITE_PAWN,
                WHITE_PAWN,
                WHITE_PAWN,
                WHITE_PAWN,
                WHITE_PAWN,
                WHITE_PAWN,
            ],
            [
                WHITE_ROOK,
                WHITE_KNIGHT,
                WHITE_BISHOP,
                WHITE_QUEEN,
                WHITE_KING,
                WHITE_BISHOP,
                WHITE_KNIGHT,
                WHITE_ROOK,
            ],
        ]
    )
    assert np.all(actual_board == expected_board)
