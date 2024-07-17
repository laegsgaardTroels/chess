import numpy as np
from ._environment import bb_to_ij, ActionFlag
from ._constants import (
    EMPTY,
    WHITE,
    BLACK,
    STATE_DTYPE,
    PIECE_NAMES,
    PIECE_STRS,
    BOARD,
    LETTERS,
    REVERSED_NUMBERS,
    MAX_PLY,
)


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


def board_flipud(board: str):
    idxs = np.flipud(np.arange(64).reshape(8, 8)).flatten()
    return "".join([board[idx] for idx in idxs])


def board_fliplr(board: str):
    idxs = np.fliplr(np.arange(64).reshape(8, 8)).flatten()
    return "".join([board[idx] for idx in idxs])


def board_rot90(board: str, k: int = 1):
    idxs = np.rot90(np.arange(64).reshape(8, 8), k=k).flatten()
    return "".join([board[idx] for idx in idxs])


def board_swapcolor(board: str):
    return board.translate(str.maketrans(TRANSLATIONTABLE))


def state_init(color: int = WHITE, board: str = BOARD, **kwargs):
    assert color in set([WHITE, BLACK])
    assert len(board) == 64
    state = np.zeros(shape=(1,), dtype=STATE_DTYPE)
    for piece_name in PIECE_NAMES:
        state[0][piece_name] = 0
    state["white_player_turn"] = color
    state["ply"] = 0
    for key, value in kwargs.items():
        state[key] = value
    cursor = 1
    for entry in board:
        for piece_name, piece_str in zip(PIECE_NAMES, PIECE_STRS):
            if entry == piece_str:
                state[0][piece_name] |= np.uint64(cursor)
                break
        cursor = cursor << 1
    return state


def state_str(state, with_ply=False):
    if isinstance(state, np.ndarray):
        state = state[0]
    s = ""
    if with_ply:
        s = s + f"Ply: {int(state['ply'])}\n"
    if state["white_player_turn"]:
        s = s + "Player: White\n"
    else:
        s = s + "Player: Black\n"
    cursor = 1
    for _, number in zip(range(8), REVERSED_NUMBERS):  # i
        s = s + str(number)
        for _ in range(8):  # j
            for piece_name, piece_str in zip(PIECE_NAMES, PIECE_STRS):
                if state[piece_name] & np.uint64(cursor):
                    s = s + piece_str
                    break
            else:
                s = s + " "
            cursor = cursor << 1
        s = s + "\n"
    s = s + " " + "".join(LETTERS)
    return s


def bitboard_str(bb):
    bb = int(bb)
    cursor = int(1)
    s = ""
    for _ in range(8):  # i
        for _ in range(8):  # j
            if cursor & bb:
                s = s + "1"
            else:
                s = s + "0"
            cursor = cursor << 1
        s += "\n"
    return s


def print_bitboard(*bbs):
    for bb in bbs:
        print()
        print(bitboard_str(bb))


def simulate_random_game(env, verbose=False):
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
    ply = 0
    for ply in range(MAX_PLY + 1):
        choices = env.actions(state)
        assert len(choices) > 0, f"\n{state_str(state)}"
        state = env.step(state, np.random.choice(choices))
        if verbose:
            print(state_str(state))
        if (
            state["is_black_checkmate"]
            or state["is_white_checkmate"]
            or state["is_draw"]
        ):
            break
    assert (
        state["is_black_checkmate"] or state["is_white_checkmate"] or state["is_draw"]
    )
    assert state["ply"] <= MAX_PLY
    return ply + 1


def all_invariants(testdata):
    """Invariant under 90 degree rotation of the board and swap of color for each rotation."""
    return [
        (color_transform(color), board_transform(board), expected_n_actions)
        for color_transform, board_transform in [
            *[
                (lambda x: x, board_transform)
                for board_transform in [
                    lambda x: x,
                    lambda x: board_rot90(x, k=1),
                    lambda x: board_rot90(x, k=2),
                    lambda x: board_rot90(x, k=3),
                ]
            ],
            *[
                (lambda x: WHITE if x == BLACK else BLACK, board_transform)
                for board_transform in [
                    lambda x: board_swapcolor(x),
                    lambda x: board_rot90(board_swapcolor(x), k=1),
                    lambda x: board_rot90(board_swapcolor(x), k=2),
                    lambda x: board_rot90(board_swapcolor(x), k=3),
                ]
            ],
        ]
        for color, board, expected_n_actions in testdata
    ]


def flipud_invariant(testdata):
    """Invariant under up/down flip of the board if one swaps the color during a flip."""
    return [
        (color_transform(color), board_transform(board), expected_n_actions)
        for color_transform, board_transform in [
            (lambda x: x, lambda x: x),
            (
                lambda x: WHITE if x == BLACK else BLACK,
                lambda x: board_flipud(board_swapcolor(x)),
            ),
        ]
        for color, board, expected_n_actions in testdata
    ]


def actions_str(actions) -> str:
    return "\n".join([f"{idx:<3}: {_action_str(a)}" for idx, a in enumerate(actions)])


def _action_str(action) -> str:  # noqa
    if action["src"] != EMPTY:
        src_i, src_j = bb_to_ij(action["src"])
        dst_i, dst_j = bb_to_ij(action["dst"])
        src_str = LETTERS[src_j] + str(REVERSED_NUMBERS[src_i])
        dst_str = LETTERS[dst_j] + str(REVERSED_NUMBERS[dst_i])
        from_to_str = src_str + " -> " + dst_str
        if action["action_flag"] == ActionFlag.move_black_rook:
            return "♜ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_black_knight:
            return "♞ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_black_bishop:
            return "♝ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_black_queen:
            return "♛ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_black_king:
            return "♚ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_black_pawn:
            return "♟ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_black_pawn_double:
            return "♟ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_rook:
            return "♖ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_knight:
            return "♘ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_bishop:
            return "♗ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_queen:
            return "♕ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_king:
            return "♔ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_pawn:
            return "♙ " + from_to_str
        elif action["action_flag"] == ActionFlag.move_white_pawn_double:
            return "♙ " + from_to_str
        elif action["action_flag"] == ActionFlag.promote_black_rook:
            return "♟ " + from_to_str + " promote to ♜"
        elif action["action_flag"] == ActionFlag.promote_black_knight:
            return "♟ " + from_to_str + " promote to ♞"
        elif action["action_flag"] == ActionFlag.promote_black_bishop:
            return "♟ " + from_to_str + " promote to ♝"
        elif action["action_flag"] == ActionFlag.promote_black_queen:
            return "♟ " + from_to_str + " promote to ♛"
        elif action["action_flag"] == ActionFlag.promote_black_pawn:
            return "♟ " + from_to_str + " promote to ♟"
        elif action["action_flag"] == ActionFlag.promote_white_rook:
            return "♙ " + from_to_str + " promote to ♖"
        elif action["action_flag"] == ActionFlag.promote_white_knight:
            return "♙ " + from_to_str + " promote to ♘"
        elif action["action_flag"] == ActionFlag.promote_white_bishop:
            return "♙ " + from_to_str + " promote to ♗"
        elif action["action_flag"] == ActionFlag.promote_white_queen:
            return "♙ " + from_to_str + " promote to ♕"
        elif action["action_flag"] == ActionFlag.promote_white_pawn:
            return "♙ " + from_to_str + " promote to ♙"
        elif action["action_flag"] == ActionFlag.move_black_pawn_en_passant:
            return "♟ " + from_to_str + " en passant"
        elif action["action_flag"] == ActionFlag.move_white_pawn_en_passant:
            return "♙ " + from_to_str + " en passant"
        else:
            raise NotImplementedError()
    elif action["action_flag"] == ActionFlag.castle_queenside_black:
        return "♜ castle queenside"
    elif action["action_flag"] == ActionFlag.castle_kingside_black:
        return "♜ castle kingside"
    elif action["action_flag"] == ActionFlag.castle_queenside_white:
        return "♖ castle queenside"
    elif action["action_flag"] == ActionFlag.castle_kingside_white:
        return "♖ castle kingside"
    else:
        raise NotImplementedError()
