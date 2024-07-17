import pytest
from chess._constants import BLACK, WHITE
from chess._environment import ActionFlag
from chess._utils import (
    state_init,
    actions_str,
)

A3 = 1 << 40
B6 = 1 << 17
NO_EN_PASSANT = 0


@pytest.mark.parametrize(
    "color,board,en_passant_square_black,en_passant_square_white,n_en_passant_actions",
    [
        (
            WHITE,
            "♜♞♝♛♚♝♞♜"
            "♟ ♟♟♟♟♟♟"
            "        "
            "♙♟      "
            "        "
            "        "
            " ♙♙♙♙♙♙♙"
            "♖♘♗♕♔♗♘♖",
            NO_EN_PASSANT,
            B6,
            1
        ),
        (
            WHITE,
            "♜♞♝♛♚♝♞♜"
            "♟ ♟♟♟♟♟♟"
            "        "
            "♙♟♙     "
            "        "
            "        "
            " ♙ ♙♙♙♙♙"
            "♖♘♗♕♔♗♘♖",
            NO_EN_PASSANT,
            B6,
            2
        ),
        (
            BLACK,
            "♜♞♝♛♚♝♞♜"
            "♟ ♟♟♟♟♟♟"
            "        "
            "        "
            "♙♟      "
            "        "
            " ♙♙♙♙♙♙♙"
            "♖♘♗♕♔♗♘♖",
            A3,
            NO_EN_PASSANT,
            1
        ),
    ],
)
def test_en_passant(
    env,
    color,
    board,
    en_passant_square_black,
    en_passant_square_white,
    n_en_passant_actions,
):
    state = state_init(
        color=color,
        board=board,
        en_passant_square_black=en_passant_square_black,
        en_passant_square_white=en_passant_square_white,
    )
    actions = env.actions(state)
    if en_passant_square_black:
        assert (
            sum(actions["action_flag"]
                == ActionFlag.move_black_pawn_en_passant)
            == n_en_passant_actions
        ), f"\n{actions_str(actions)}"
    else:
        assert (
            sum(actions["action_flag"]
                == ActionFlag.move_white_pawn_en_passant)
            == n_en_passant_actions
        ), f"\n{actions_str(actions)}"
