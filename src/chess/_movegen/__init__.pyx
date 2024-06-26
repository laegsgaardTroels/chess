import cython
import numpy as np
cimport numpy as np
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
    NO_CASTLING,
    NO_PROMOTION,
    STATE_DTYPE,
    ACTION_DTYPE,
    WHITE,
    BLACK,
)

cdef packed struct Castling:
    np.npy_bool left_black
    np.npy_bool right_black
    np.npy_bool left_white
    np.npy_bool right_white


cdef packed struct Promotion:
    np.npy_bool rook
    np.npy_bool knight
    np.npy_bool bishop
    np.npy_bool queen
    np.npy_bool pawn


cdef packed struct State:
    np.npy_bool color
    long[8][8] board
    Castling castling
    np.npy_bool white_checkmate
    np.npy_bool black_checkmate
    np.npy_bool draw


cdef packed struct Position:
    long i
    long j


cdef packed struct Action:
    long piece
    Position src
    Position dst
    Castling castling
    Promotion promotion


def actions(state):
    actions = pseudo_actions(state)
    next_state = step(state, actions)
    return actions[_not_in_enemy_attackset(next_state, state["color"])]


def _not_in_enemy_attackset(state, color):
    ic = np.empty(shape=state.shape, dtype=bool)
    for idx in range(len(state)):
        s = state[[idx]]
        pa = pseudo_actions(s)
        ns = step(s, pa)
        if color == WHITE:
            ic[idx] = (ns["board"] == WHITE_KING).sum(axis=(1,2)).all()
        elif color == BLACK:
            ic[idx] = (ns["board"] == BLACK_KING).sum(axis=(1,2)).all()
        else:
            raise NotImplementedError()
    return ic


def step(state, action):
    assert len(state) == 1
    assert len(action) > 0
    action = action.reshape(-1)
    assert state.shape
    assert action.shape
    return _step(state[0], action)


def pseudo_actions(state):
    return _pseudo_actions(state[0])


def _step(State state, Action [:] action):
    cdef np.ndarray[State, ndim=1] new_state = np.empty(action.shape[0], dtype=STATE_DTYPE)
    cdef State [:] new_state_view = new_state
    for i in range(action.shape[0]):
        new_state_view[i] = _step_scalar(state, action[i])
    return new_state


def _pseudo_actions(State state):
    cdef np.ndarray[Action, ndim=1] actions = np.empty(100000, dtype=ACTION_DTYPE)
    cdef Action [:] actions_view = actions
    cdef int n = 0
    cdef long i,j

    for i in range(8):
        for j in range(8):
            src = Position(i, j)
            if state.board[i][j] == EMPTY:
                continue
            elif state.color == WHITE:
                if state.board[i][j] == WHITE_ROOK:
                    n = rook_pseudo_actions(n, WHITE_ROOK, src, state, actions_view)
                elif state.board[i][j] == WHITE_KNIGHT:
                    n = knight_pseudo_actions(n, WHITE_KNIGHT, src, state, actions_view)
                elif state.board[i][j] == WHITE_BISHOP:
                    n = bishop_pseudo_actions(n, WHITE_BISHOP, src, state, actions_view)
                elif state.board[i][j] == WHITE_QUEEN:
                    n = queen_pseudo_actions(n, WHITE_QUEEN, src, state, actions_view)
                elif state.board[i][j] == WHITE_KING:
                    n = king_pseudo_actions(n, WHITE_KING, src, state, actions_view)
                elif state.board[i][j] == WHITE_PAWN:
                    n = pawn_pseudo_actions(n, WHITE_PAWN, src, state, actions_view)
            elif state.color == BLACK:
                if state.board[i][j] == BLACK_ROOK:
                    n = rook_pseudo_actions(n, BLACK_ROOK, src, state, actions_view)
                elif state.board[i][j] == BLACK_KNIGHT:
                    n = knight_pseudo_actions(n, BLACK_KNIGHT, src, state, actions_view)
                elif state.board[i][j] == BLACK_BISHOP:
                    n = bishop_pseudo_actions(n, BLACK_BISHOP, src, state, actions_view)
                elif state.board[i][j] == BLACK_QUEEN:
                    n = queen_pseudo_actions(n, BLACK_QUEEN, src, state, actions_view)
                elif state.board[i][j] == BLACK_KING:
                    n = king_pseudo_actions(n, BLACK_KING, src, state, actions_view)
                elif state.board[i][j] == BLACK_PAWN:
                    n = pawn_pseudo_actions(n, BLACK_PAWN, src, state, actions_view)
            else:
                raise NotImplementedError()

    if state.color == WHITE:
        n = white_castling_queenside(n, WHITE_ROOK, src, state, actions_view)
        n = white_castling_kingside(n, WHITE_ROOK, src, state, actions_view)
    elif state.color == BLACK:
        n = black_castling_queenside(n, BLACK_ROOK, src, state, actions_view)
        n = black_castling_kingside(n, BLACK_ROOK, src, state, actions_view)
    else:
        raise NotImplementedError()

    return actions[:n]


def _step_scalar(State state, Action action):
    state.color = not state.color
    if action.castling.left_black:
        state.board[0][0] = EMPTY
        state.board[0][4] = EMPTY
        state.board[0][2] = BLACK_ROOK
        state.board[0][3] = BLACK_KING
        state.castling.left_black = action.castling.left_black
    elif action.castling.right_black:
        state.board[0][7] = EMPTY
        state.board[0][4] = EMPTY
        state.board[0][5] = BLACK_ROOK
        state.board[0][6] = BLACK_KING
        state.castling.right_black = action.castling.right_black
    elif action.castling.left_white:
        state.board[7][0] = EMPTY
        state.board[7][4] = EMPTY
        state.board[7][2] = WHITE_ROOK
        state.board[7][3] = WHITE_KING
        state.castling.left_white = action.castling.left_white
    elif action.castling.right_white:
        state.board[7][7] = EMPTY
        state.board[7][4] = EMPTY
        state.board[7][5] = WHITE_ROOK
        state.board[7][6] = WHITE_KING
        state.castling.right_white = action.castling.right_white
    elif action.piece == WHITE_PAWN:
        state.board[action.src.i][action.src.j] = EMPTY
        if action.promotion.rook:
            state.board[action.dst.i][action.dst.j] = WHITE_ROOK
        elif action.promotion.knight:
            state.board[action.dst.i][action.dst.j] = WHITE_KNIGHT
        elif action.promotion.bishop:
            state.board[action.dst.i][action.dst.j] = WHITE_BISHOP
        elif action.promotion.queen:
            state.board[action.dst.i][action.dst.j] = WHITE_QUEEN
        elif action.promotion.pawn:
            state.board[action.dst.i][action.dst.j] = WHITE_PAWN
        else:
            state.board[action.dst.i][action.dst.j] = WHITE_PAWN
    elif action.piece == BLACK_PAWN:
        state.board[action.src.i][action.src.j] = EMPTY
        if action.promotion.rook:
            state.board[action.dst.i][action.dst.j] = BLACK_ROOK
        elif action.promotion.knight:
            state.board[action.dst.i][action.dst.j] = BLACK_KNIGHT
        elif action.promotion.bishop:
            state.board[action.dst.i][action.dst.j] = BLACK_BISHOP
        elif action.promotion.queen:
            state.board[action.dst.i][action.dst.j] = BLACK_QUEEN
        elif action.promotion.pawn:
            state.board[action.dst.i][action.dst.j] = BLACK_PAWN
        else:
            state.board[action.dst.i][action.dst.j] = BLACK_PAWN
    elif action.piece == BLACK_KING:
        state.board[action.src.i][action.src.j] = EMPTY
        state.castling.left_black = True
        state.castling.right_black = True
        state.board[action.dst.i][action.dst.j] = action.piece
    elif action.piece == WHITE_KING:
        state.board[action.src.i][action.src.j] = EMPTY
        state.castling.left_white = True
        state.castling.right_white = True
        state.board[action.dst.i][action.dst.j] = action.piece
    else:
        state.board[action.src.i][action.src.j] = EMPTY
        state.board[action.dst.i][action.dst.j] = action.piece
    state.white_checkmate = white_checkmate(state)
    state.black_checkmate = black_checkmate(state)
    state.draw = draw(state)
    return state


def outside_board(Position dst):
    if dst.i < 0 or dst.j < 0:
        return True
    elif dst.i > 7 or dst.j > 7:
        return True
    else:
        return False


def own_piece_at_dst(State state, Position dst):
    board = state.board[dst.i][dst.j]
    if state.color:
        return board >= 7
    else:
        return ((0 < board) & (board < 7))


def enemy_piece_at_dst(State state, Position dst):
    board = state.board[dst.i][dst.j]
    if state.color:
        return (0 < board) & (board < 7)
    else:
        return board >= 7


def black_castling_queenside(int n, long piece, Position src, State state, Action [:] actions_view):
    if (
        state.color == BLACK
        and state.board[0][0] == BLACK_ROOK
        and state.board[0][1] == EMPTY
        and state.board[0][2] == EMPTY
        and state.board[0][3] == EMPTY
        and state.board[0][4] == BLACK_KING
        and not state.castling.left_black
    ):
        actions_view[n] = Action(piece, src, src, Castling(True, False, False, False), Promotion(False, False, False, False, False))
        n = n + 1
    return n


def black_castling_kingside(int n, long piece, Position src, State state, Action [:] actions_view):
    if (
        state.color == BLACK
        and state.board[0][4] == BLACK_KING
        and state.board[0][5] == EMPTY
        and state.board[0][6] == EMPTY
        and state.board[0][7] == BLACK_ROOK
        and not state.castling.left_black
    ):
        actions_view[n] = Action(piece, src, src, Castling(False, True, False, False), Promotion(False, False, False, False, False))
        n = n + 1
    return n


def white_castling_queenside(int n, long piece, Position src, State state, Action [:] actions_view):
    if (
        state.color == WHITE
        and state.board[7][0] == WHITE_ROOK
        and state.board[7][1] == EMPTY
        and state.board[7][2] == EMPTY
        and state.board[7][3] == EMPTY
        and state.board[7][4] == WHITE_KING
        and not state.castling.left_black
    ):
        actions_view[n] = Action(piece, src, src, Castling(False, False, True, False), Promotion(False, False, False, False, False))
        n = n + 1
    return n


def white_castling_kingside(int n, long piece, Position src, State state, Action [:] actions_view):
    if (
        state.color == WHITE
        and state.board[7][4] == WHITE_KING
        and state.board[7][5] == EMPTY
        and state.board[7][6] == EMPTY
        and state.board[7][7] == WHITE_ROOK
        and not state.castling.left_black
    ):
        actions_view[n] = Action(piece, src, src, Castling(False, False, False, True), Promotion(False, False, False, False, False))
        n = n + 1
    return n


def rook_pseudo_actions(int n, long piece, Position src, State state, Action [:] actions_view):
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        for step in range(1, 8):
            dst = Position(src.i + step * di, src.j + step * dj)
            if outside_board(dst) or own_piece_at_dst(state, dst):
                break
            if state.board[dst.i][dst.j] == EMPTY:
                actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                n = n + 1
            elif enemy_piece_at_dst(state, dst):
                actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                n = n + 1
                break
            else:
                raise NotImplementedError()
    return n
 
 
def knight_pseudo_actions(int n, long piece, Position src, State state, Action [:] actions_view):
     for di, dj in [
         (-2, -1),
         (2, 1),
         (2, -1),
         (-2, 1),
         (-1, -2),
         (1, 2),
         (1, -2),
         (-1, 2),
     ]:
        dst = Position(src.i + di, src.j + dj)
        if outside_board(dst) or own_piece_at_dst(state, dst):
            continue
        else:
            actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
            n = n + 1
     return n


def bishop_pseudo_actions(int n, long piece, Position src, State state, Action [:] actions_view):
    for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        for step in range(1, 8):
            dst = Position(src.i + step * di, src.j + step * dj)
            if outside_board(dst) or own_piece_at_dst(state, dst):
                break
            elif not state.board[dst.i][dst.j]:
                actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                n = n + 1
            else:
                actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                n = n + 1
                break
    return n


def queen_pseudo_actions(int n, long piece, Position src, State state, Action [:] actions_view):
    n = bishop_pseudo_actions(n, piece, src, state, actions_view)
    return rook_pseudo_actions(n, piece, src, state, actions_view)


def king_pseudo_actions(int n, long piece, Position src, State state, Action [:] actions_view):
    for di, dj in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        dst = Position(src.i + di, src.j + dj)
        if outside_board(dst) or own_piece_at_dst(state, dst):
            continue
        else:
            actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
            n = n + 1
    return n


def pawn_pseudo_actions(int n, long piece, Position src, State state, Action [:] actions_view):
    if state.color:
        for di, dj in [(-1, 0), (-2, 0)]:
            dst = Position(src.i + di, src.j + dj)
            if outside_board(dst) or own_piece_at_dst(state, dst):
                break
            elif src.i != 6 and di == -2:
                break
            elif not state.board[dst.i][dst.j]:
                if dst.i == 0:
                    actions_view[n + 0] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(True, False, False, False, False))
                    actions_view[n + 1] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, True, False, False, False))
                    actions_view[n + 2] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, True, False, False))
                    actions_view[n + 3] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, True, False))
                    actions_view[n + 4] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, True))
                    n = n + 5
                else:
                    actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                    n = n + 1
            else:
                break
        for di, dj in [(-1, 1), (-1, -1)]:
            dst = Position(src.i + di, src.j + dj)
            if outside_board(dst):
                continue
            if enemy_piece_at_dst(state, dst):
                if dst.i == 0:
                    actions_view[n + 0] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(True, False, False, False, False))
                    actions_view[n + 1] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, True, False, False, False))
                    actions_view[n + 2] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, True, False, False))
                    actions_view[n + 3] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, True, False))
                    actions_view[n + 4] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, True))
                    n = n + 5
                else:
                    actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                    n = n + 1
    else:
        for di, dj in [(1, 0), (2, 0)]:
            dst = Position(src.i + di, src.j + dj)
            if outside_board(dst) or own_piece_at_dst(state, dst):
                break
            elif src.i != 1 and di == 2:
                break
            elif not state.board[dst.i][dst.j]:
                if dst.i == 7:
                    actions_view[n + 0] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(True, False, False, False, False))
                    actions_view[n + 1] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, True, False, False, False))
                    actions_view[n + 2] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, True, False, False))
                    actions_view[n + 3] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, True, False))
                    actions_view[n + 4] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, True))
                    n = n + 5
                else:
                    actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                    n = n + 1
            else:
                break
        for di, dj in [(1, 1), (1, -1)]:
            dst = Position(src.i + di, src.j + dj)
            if outside_board(dst):
                continue
            if enemy_piece_at_dst(state, dst):
                if dst.i == 7:
                    actions_view[n + 0] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(True, False, False, False, False))
                    actions_view[n + 1] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, True, False, False, False))
                    actions_view[n + 2] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, True, False, False))
                    actions_view[n + 3] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, True, False))
                    actions_view[n + 4] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, True))
                    n = n + 5
                else:
                    actions_view[n] = Action(piece, src, dst, Castling(False, False, False, False), Promotion(False, False, False, False, False))
                    n = n + 1
    return n


# terminal 


def draw(state):
    return np.isin(state["board"], [EMPTY, WHITE_KING, BLACK_KING]).all(axis=None)


def white_checkmate(state):
    return False


def black_checkmate(state):
    return False



# utilities


def alphabeta(
    state,
    depth,
    piece_value,
    alpha=-np.inf,
    beta=np.inf,
    maximizing_player=True,
):
    """Minimax with alpha-beta pruning."""

    if depth == 0:
        value = state_value(state, piece_value)
    else:
        if maximizing_player:
            value = -np.inf
            for action in actions(state):
                new_state = step(state, action)
                new_value = alphabeta(new_state, depth - 1, piece_value, alpha, beta, False)
                value = max(value, new_value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = np.inf
            for action in actions(state):
                new_state = step(state, action)
                new_value = alphabeta(new_state, depth - 1, piece_value, alpha, beta, True)
                value = min(value, new_value)
                beta = min(beta, value)
                if alpha >= beta:
                    break
    return value


def state_value(state, piece_value):
    total_value = 0
    for piece, value in piece_value.items():
        total_value = total_value + np.sum(state["board"] == piece) * value
    return total_value
