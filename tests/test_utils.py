from chess._utils import state_init, state_str


def test_state_str():
    state = state_init(
        board=(
            "♜♞♝♛♚♝♞♜"
            "♟♟♟♟♟♟♟♟"
            "        "
            "        "
            "        "
            "        "
            "♙♙♙♙♙♙♙♙"
            "♖♘♗♕♔♗♘♖"
        )
    )
    actual_state_str = state_str(state)
    expected_state_str = (
        "Player: White\n"
        "8♜♞♝♛♚♝♞♜\n"
        "7♟♟♟♟♟♟♟♟\n"
        "6        \n"
        "5        \n"
        "4        \n"
        "3        \n"
        "2♙♙♙♙♙♙♙♙\n"
        "1♖♘♗♕♔♗♘♖\n"
        " abcdefgh"
    )
    assert actual_state_str == expected_state_str
