import numpy as np
from chess._constants import (
    WHITE,
    BOARD,
    NO_CASTLING,
    STATE_DTYPE,
    PIECE_STRS,
    LETTERS,
    REVERSED_NUMBERS,
)


def init_state(color=WHITE, board=BOARD, castling=NO_CASTLING):
    assert len(board) == 64
    assert len(castling) == 4
    state = np.empty(1, dtype=STATE_DTYPE)
    state[0]["board"] = 0
    state[0]["color"] = bool(color)
    state[0]["castling"] = castling
    for entry_idx, entry in enumerate(board):
        i = entry_idx // 8
        j = entry_idx % 8
        for piece_idx, piece_str in enumerate(PIECE_STRS.values(), 1):
            if entry == piece_str:
                state[0]["board"][i, j] = piece_idx
    assert state[0]["board"].shape == (8, 8)
    return state


def boardstr(state):
    assert state[0]["board"].shape == (8, 8), f"{state[0]['board']=}"
    s = ""
    for i in range(8):
        for j in range(8):
            for piece_idx, piece_str in enumerate(PIECE_STRS.values(), 1):
                try:
                    if state[0]["board"][i, j] == piece_idx:
                        s = s + piece_str
                        break
                except Exception as exec:
                    raise ValueError(
                        f"Something went wrong {state['board']=}, "
                        f"{i=}, {j=} {state['board'][i, j]=}"
                    ) from exec
            else:
                s = s + " "
    return s


def statestr(state):
    s = ""
    if state["color"]:
        s = s + "Color: White\n"
    else:
        s = s + "Color: Black\n"
    b = boardstr(state)
    for line, x in enumerate(range(0, 64, 8)):
        line_str = str(8 - line)
        s = s + line_str + b[x: x + 8] + "\n"
    s = s + " abcdefgh"
    return s


def actionstr(action):
    if action["castling"]["left_black"]:
        return PIECE_STRS[action["piece"]] + " " + "castling left"
    elif action["castling"]["right_black"]:
        return PIECE_STRS[action["piece"]] + " " + "castling right"
    elif action["castling"]["left_white"]:
        return PIECE_STRS[action["piece"]] + " " + "castling left"
    elif action["castling"]["right_white"]:
        return PIECE_STRS[action["piece"]] + " " + "castling right"
    elif action["promotion"]["rook"]:
        return PIECE_STRS[action["piece"]] + " " + "promotion rook"
    elif action["promotion"]["knight"]:
        return PIECE_STRS[action["piece"]] + " " + "promotion knight"
    elif action["promotion"]["bishop"]:
        return PIECE_STRS[action["piece"]] + " " + "promotion bishop"
    elif action["promotion"]["queen"]:
        return PIECE_STRS[action["piece"]] + " " + "promotion queen"
    elif action["promotion"]["pawn"]:
        return PIECE_STRS[action["piece"]] + " " + "promotion pawn"
    else:
        src_str = LETTERS[action["src"]["j"]] + str(
            REVERSED_NUMBERS[action["src"]["i"]]
        )
        dst_str = LETTERS[action["dst"]["j"]] + str(
            REVERSED_NUMBERS[action["dst"]["i"]]
        )
        return PIECE_STRS[action["piece"]] + " " + src_str + " -> " + dst_str
