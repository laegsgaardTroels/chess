import pytest
from typing import NamedTuple, Literal
import numpy as np
from chess import _movegen
from chess import _utils
from chess._constants import NO_CASTLING, BLACK, WHITE, PIECE_STRS


TRANSLATIONTABLE = {
    "♜": "♖",
    "♞": "♘",
    "♝": "♗",
    "♛": "♕",
    "♚": "♔",
    "♟": "♙",
    "♖": "♜",
    "♘": "♞",
    "♗": "♝",
    "♕": "♛",
    "♔": "♚",
    "♙": "♟",
}


def init_state_flipud(color, board, castling):
    return _utils.init_state(
        color=not color,
        board="".join(
            reversed([board[idx : idx + 8] for idx in range(0, 64, 8)])
        ).translate(str.maketrans(TRANSLATIONTABLE)),
        castling=castling[2:4] + castling[0:2],
    )


def init_state_fliplr(color, board, castling):
    return _utils.init_state(
        color=color,
        board="".join(
            ["".join(reversed(board[idx : idx + 8])) for idx in range(0, 64, 8)]
        ),
        castling=castling,
    )


class NumberOfActionsTestData(NamedTuple):
    # Expected number of actions for each piece (default=0)
    expected_number_of_actions: dict[str, int]

    # State
    color: Literal[0, 1]
    board: str
    castling: tuple[bool, bool, bool, bool] = NO_CASTLING

    # Should a test be done with the same counts where the
    # board is fliped up/down (ud) + color and left/right (lr)
    # e.g. is the actions symmetric ud and lr.
    flipud: bool = True
    fliplr: bool = True

    # Description of the position
    description: str = ""


class NumberOfActionsTestParams(NamedTuple):
    # State
    state: np.void

    # Expected number of actions for each piece (default=0)
    expected_number_of_actions: dict[str, int]


def build_number_of_actions_params(
    testdatas: list[NumberOfActionsTestData],
) -> list[NumberOfActionsTestParams]:
    params = []
    for testdata in testdatas:
        # Original
        params.append(
            NumberOfActionsTestParams(
                state=_utils.init_state(
                    color=testdata.color,
                    board=testdata.board,
                    castling=testdata.castling,
                ),
                expected_number_of_actions=testdata.expected_number_of_actions,
            )
        )

        # Flip up/down (ud) + color
        if testdata.flipud:
            params.append(
                NumberOfActionsTestParams(
                    state=init_state_flipud(
                        color=testdata.color,
                        board=testdata.board,
                        castling=testdata.castling,
                    ),
                    expected_number_of_actions={
                        TRANSLATIONTABLE[k]: v
                        for k, v in testdata.expected_number_of_actions.items()
                    },
                )
            )

        # Flip left/right (lr)
        if testdata.fliplr:
            params.append(
                NumberOfActionsTestParams(
                    state=init_state_fliplr(
                        color=testdata.color,
                        board=testdata.board,
                        castling=testdata.castling,
                    ),
                    expected_number_of_actions=testdata.expected_number_of_actions,
                )
            )
    return params


@pytest.mark.parametrize(
    "state,expected_number_of_actions",
    build_number_of_actions_params(
        [
            NumberOfActionsTestData(
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
                expected_number_of_actions={
                    "♘": 4,
                    "♙": 16,
                },
                description="Starting position",
            ),
            NumberOfActionsTestData(
                color=BLACK,
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
                expected_number_of_actions={
                    "♞": 4,
                    "♟": 16,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "♜♞♝♛♚♝♞♜"
                    "♟♟♟♟♟♟♟♟"
                    "        "
                    "        "
                    "        "
                    "        "
                    "♙♙♙♙ ♙♙♙"
                    "♖♘♗♕♔♗♘♖"
                ),
                expected_number_of_actions={
                    "♘": 5,
                    "♗": 5,
                    "♕": 4,
                    "♔": 1,
                    "♙": 14,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "♜♞♝♛♚♝♞♜"
                    "♟♟♟♟♟♟♟♟"
                    "        "
                    "        "
                    "        "
                    "        "
                    "♙♙♙♙♙♙♙ "
                    "♖♘♗♕♔♗♘♖"
                ),
                expected_number_of_actions={
                    "♖": 6,
                    "♘": 4,
                    "♙": 14,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "♖       "
                ),
                expected_number_of_actions={
                    "♖": 14,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "  ♖     "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♖": 14,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "  ♖ ♟   "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♖": 11,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "  ♟     "
                    "        "
                    "  ♖     "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♖": 13,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "  ♖     "
                    "        "
                    "  ♟     "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♖": 12,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "♖   ♔   "
                ),
                castling=(False, False, False, False),
                expected_number_of_actions={
                    "♔": 5,
                    "♖": 10,
                },
                fliplr=False,
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "    ♔  ♖"
                ),
                castling=(False, False, False, False),
                fliplr=False,
                expected_number_of_actions={
                    "♔": 5,
                    "♖": 9,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "      ♘ "
                ),
                expected_number_of_actions={
                    "♘": 3,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "   ♘    "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♘": 8,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "       ♘"
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♘": 3,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "     ♟  "
                    "       ♘"
                    "     ♟  "
                    "      ♟ "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♘": 3,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "     ♗  "
                ),
                expected_number_of_actions={
                    "♗": 7,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "    ♗   "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♗": 13,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "    ♗   "
                    "   ♟    "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♗": 10,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "   ♕    "
                ),
                expected_number_of_actions={
                    "♕": 21,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "    ♟   "
                    "   ♕    "
                ),
                expected_number_of_actions={
                    "♕": 18,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "    ♔   "
                ),
                expected_number_of_actions={
                    "♔": 5,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "   ♙♙♙  "
                    "   ♙♔♙  "
                ),
                expected_number_of_actions={
                    "♔": 0,
                    "♙": 6,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "   ♙♙♙  "
                    "   ♙♔   "
                    "   ♙♙♙  "
                    "        "
                ),
                expected_number_of_actions={
                    "♔": 1,
                    "♙": 4,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "   ♟    "
                    "    ♔   "
                ),
                expected_number_of_actions={
                    "♔": 5,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    " ♟ ♟    "
                    "  ♙     "
                    "        "
                ),
                expected_number_of_actions={
                    "♙": 4,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    " ♟♟♟    "
                    "  ♙     "
                    "        "
                ),
                expected_number_of_actions={
                    "♙": 2,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    " ♟♙♟    "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♙": 1,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "  ♟     "
                    "  ♙     "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♙": 0,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "  ♙     "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♙": 5,
                },
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "        "
                    "  ♙♙    "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={
                    "♙": 10,
                },
            ),
        ]
    ),
)
def test_expected_number_of_pseudo_actions(state, expected_number_of_actions):
    actions = _movegen.pseudo_actions(state)
    for piece, piece_str in PIECE_STRS.items():
        actual = np.sum(actions["piece"] == piece)
        expected = expected_number_of_actions.get(piece_str, 0)
        assert (
            actual == expected
        ), f"\n{_utils.statestr(state)}\n{str(actions[actions['piece'] == piece])}"


@pytest.mark.parametrize(
    "state,expected_number_of_actions",
    build_number_of_actions_params(
        [
            NumberOfActionsTestData(
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
                expected_number_of_actions={
                    "♘": 4,
                    "♙": 16,
                },
                description="Starting position",
            ),
            NumberOfActionsTestData(
                color=WHITE,
                board=(
                    "♜♞♝ ♚♝♞♜"
                    "♟♟♟♟ ♟♟♟"
                    "        "
                    "    ♟   "
                    "      ♙♛"
                    "     ♙  "
                    "♙♙♙♙♙  ♙"
                    "♖♘♗♕♔♗♘♖"
                ),
                expected_number_of_actions={},
                description="Checkmate: Fool's mate",
            ),
            NumberOfActionsTestData(
                color=BLACK,
                board=(
                    "        "
                    "        "
                    "♚♕♔     "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={},
                description="Checkmate: Support mate",
            ),
            NumberOfActionsTestData(
                color=BLACK,
                board=(
                    "        "
                    "        "
                    "     ♔ ♚"
                    "        "
                    "        "
                    "        "
                    "        "
                    "       ♕"
                ),
                expected_number_of_actions={},
                description="Checkmate: Right triangle mate",
            ),
            NumberOfActionsTestData(
                color=BLACK,
                board=(
                    "      ♚♖"
                    "      ♙ "
                    "     ♔  "
                    "        "
                    "        "
                    "        "
                    "        "
                    "        "
                ),
                expected_number_of_actions={},
                description="Anderssen's mate",
            ),
        ]
    ),
)
def test_expected_number_of_actions(state, expected_number_of_actions):
    actions = _movegen.actions(state)
    for piece, piece_str in PIECE_STRS.items():
        actual = np.sum(actions["piece"] == piece)
        expected = expected_number_of_actions.get(piece_str, 0)
        assert (
            actual == expected
        ), f"\npiece={PIECE_STRS[piece]}\n{_utils.statestr(state)}\n{str(actions[actions['piece'] == piece])}"


#
#
# class StepSrcDstTestData(NamedTuple):
#     # Expected destination state
#     expected_dst_white_player_turn: bool
#     expected_dst_board: str
#     expected_dst_castling: tuple[bool]
#
#     # Source state
#     src_white_player_turn: bool
#     src_board: str
#     src_castling: tuple[bool]
#
#     # Action
#     piece: int
#     src: tuple[int]
#     dst: tuple[int]
#     castling: tuple[bool, bool, bool, bool] = ch.NO_CASTLING
#     promotion: tuple[bool, bool, bool, bool, bool] = ch.NO_PROMOTION
#
#     # Should a test be done with the same counts where the
#     # board is fliped up/down (ud) and left/right (lr)
#     # e.g. is the actions symmetric ud and lr.
#     flipud: bool = True
#     fliplr: bool = True
#
#
# class StepSrcDstTestParams(NamedTuple):
#     # Expected to state
#     expected_dst_state: np.void
#
#     # State
#     src_state: np.void
#
#     # Action
#     action: np.array
#
#
# def build_step_from_to_test_params(
#     testdatas: list[StepSrcDstTestData],
# ) -> list[StepSrcDstTestParams]:
#     params = []
#     strs_piece = {v: k for k, v in ch.PIECE_STRS.items()}
#     for testdata in testdatas:
#         params.append(
#             StepSrcDstTestParams(
#                 expected_dst_state=ch.init_state(
#                     white_player_turn=testdata.expected_dst_white_player_turn,
#                     board=testdata.expected_dst_board,
#                     castling=testdata.expected_dst_castling,
#                 ),
#                 src_state=ch.init_state(
#                     white_player_turn=testdata.src_white_player_turn,
#                     board=testdata.src_board,
#                     castling=testdata.src_castling,
#                 ),
#                 action=np.void(
#                     (
#                         strs_piece[testdata.piece],
#                         testdata.src,
#                         testdata.dst,
#                         testdata.castling,
#                         testdata.promotion,
#                     ),
#                     dtype=ch.ACTION_DTYPE,
#                 ),
#             )
#         )
#         if testdata.flipud:
#             params.append(
#                 StepSrcDstTestParams(
#                     expected_dst_state=init_state_flipud(
#                         white_player_turn=testdata.expected_dst_white_player_turn,
#                         board=testdata.expected_dst_board,
#                         castling=testdata.expected_dst_castling,
#                     ),
#                     src_state=init_state_flipud(
#                         white_player_turn=testdata.src_white_player_turn,
#                         board=testdata.src_board,
#                         castling=testdata.src_castling,
#                     ),
#                     action=np.void(
#                         (
#                             strs_piece[TRANSLATIONTABLE[testdata.piece]],
#                             (7 - testdata.src[0], testdata.src[1]),
#                             (7 - testdata.dst[0], testdata.dst[1]),
#                             testdata.castling[2:4] + testdata.castling[0:2],
#                             testdata.promotion,
#                         ),
#                         dtype=ch.ACTION_DTYPE,
#                     ),
#                 )
#             )
#         if testdata.fliplr:
#             params.append(
#                 StepSrcDstTestParams(
#                     expected_dst_state=init_state_fliplr(
#                         white_player_turn=testdata.expected_dst_white_player_turn,
#                         board=testdata.expected_dst_board,
#                         castling=testdata.expected_dst_castling,
#                     ),
#                     src_state=init_state_fliplr(
#                         white_player_turn=testdata.src_white_player_turn,
#                         board=testdata.src_board,
#                         castling=testdata.src_castling,
#                     ),
#                     action=np.void(
#                         (
#                             strs_piece[testdata.piece],
#                             (testdata.src[0], 7 - testdata.src[1]),
#                             (testdata.dst[0], 7 - testdata.dst[1]),
#                             testdata.castling,
#                             testdata.promotion,
#                         ),
#                         dtype=ch.ACTION_DTYPE,
#                     ),
#                 )
#             )
#     return params
#
#
# @pytest.mark.parametrize(
#     "expected_dst_state,state,action",
#     build_step_from_to_test_params(
#         [
#             *[
#                 StepSrcDstTestData(
#                     expected_dst_white_player_turn=False,
#                     expected_dst_board=(
#                         f"♜{promotion}♝♛♚♝♞♜"
#                         "♟ ♟♟♟♟♟♟"
#                         "        "
#                         "        "
#                         "        "
#                         "        "
#                         "♙ ♙♙♙♙♙♙"
#                         "♖♘♗♕♔♗♘♖"
#                     ),
#                     expected_dst_castling=ch.NO_CASTLING,
#                     src_white_player_turn=True,
#                     src_board=(
#                         "♜ ♝♛♚♝♞♜"
#                         "♟♙♟♟♟♟♟♟"
#                         "        "
#                         "        "
#                         "        "
#                         "        "
#                         "♙ ♙♙♙♙♙♙"
#                         "♖♘♗♕♔♗♘♖"
#                     ),
#                     src_castling=ch.NO_CASTLING,
#                     piece="♙",
#                     src=(1, 1),
#                     dst=(0, 1),
#                     promotion=tuple(pidx == idx for pidx in range(5)),
#                 )
#                 for idx, promotion in enumerate(["♖", "♘", "♗", "♕", "♙"])
#             ]
#         ]
#     ),
# )
# def test_src_dst_step(expected_dst_state, state, action):
#     actual_to_state = ch.step(state, action)
#     assert actual_to_state == expected_dst_state, (
#         f"\nactual=\n{ch.statestr(actual_to_state)}\n\n"
#         f"expected=\n{ch.statestr(expected_dst_state)}"
#     )
#
#
