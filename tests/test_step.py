from chess import actions, step
from chess import _utils
from chess._constants import WHITE


def test_step():
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

    a = actions(state)

    step(state, a)
