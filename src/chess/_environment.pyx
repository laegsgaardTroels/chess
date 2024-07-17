#cython: language_level=3
#cython: linetrace=True, profile=True, nonecheck=False, boundscheck=False, wraparound=False, cdivision=True
import numpy as np
cimport numpy as cnp
from libcpp.vector cimport vector as cpp_vector
from libcpp.unordered_map cimport unordered_map as cpp_map

cnp.import_array()

ctypedef unsigned long long Bitboard

cdef packed struct State:
    # The state should encode all the information to start the game in a given board configuration.
    # The board has 2 representations:
    # - bitboards representation (uint64, (12,))
    # - board representation (long[8][8])
    cnp.npy_bool white_player_turn
    Bitboard black_rook
    Bitboard black_knight
    Bitboard black_bishop
    Bitboard black_queen
    Bitboard black_king
    Bitboard black_pawn
    Bitboard white_rook
    Bitboard white_knight
    Bitboard white_bishop
    Bitboard white_queen
    Bitboard white_king
    Bitboard white_pawn

    cnp.npy_bool has_black_king_moved
    cnp.npy_bool has_white_king_moved
    
    cnp.npy_bool has_black_queenside_rook_moved
    cnp.npy_bool has_black_kingside_rook_moved
    cnp.npy_bool has_white_queenside_rook_moved
    cnp.npy_bool has_white_kingside_rook_moved

    # A half-move
    Bitboard ply

    # A square with the possibility of en passant
    Bitboard en_passant_square_black
    Bitboard en_passant_square_white

    cnp.npy_bool is_white_check
    cnp.npy_bool is_black_check
    cnp.npy_bool is_white_checkmate
    cnp.npy_bool is_black_checkmate
    cnp.npy_bool is_draw


cdef packed struct Action:
    # The action should encode all the information needed to transition between possible states.

    # source (uint64)
    Bitboard src

    # destination (uint64)
    Bitboard dst

    # type of action
    long flag


cpdef enum ActionFlag:
    move_black_rook = 0
    move_black_knight
    move_black_bishop
    move_black_queen
    move_black_king
    move_black_pawn
    move_black_pawn_double
    move_black_pawn_en_passant

    move_white_rook
    move_white_knight
    move_white_bishop
    move_white_queen
    move_white_king
    move_white_pawn
    move_white_pawn_double
    move_white_pawn_en_passant

    castle_queenside_black
    castle_kingside_black
    castle_queenside_white
    castle_kingside_white

    promote_black_rook
    promote_black_knight
    promote_black_bishop
    promote_black_queen
    promote_black_pawn

    promote_white_rook
    promote_white_knight
    promote_white_bishop
    promote_white_queen
    promote_white_pawn


STATE_DTYPE = [
    ("white_player_turn", "?"),
    ("black_rook", "<u8"),
    ("black_knight", "<u8"),
    ("black_bishop", "<u8"),
    ("black_queen", "<u8"),
    ("black_king", "<u8"),
    ("black_pawn", "<u8"),
    ("white_rook", "<u8"),
    ("white_knight", "<u8"),
    ("white_bishop", "<u8"),
    ("white_queen", "<u8"),
    ("white_king", "<u8"),
    ("white_pawn", "<u8"),
    ("has_black_king_moved", "?"),
    ("has_white_king_moved", "?"),
    ("has_black_queenside_rook_moved", "?"),
    ("has_black_kingside_rook_moved", "?"),
    ("has_white_queenside_rook_moved", "?"),
    ("has_white_kingside_rook_moved", "?"),
    ("ply", "<u8"),
    ("en_passant_square_black", "<u8"),
    ("en_passant_square_white", "<u8"),
    ("is_white_check", "?"),
    ("is_black_check", "?"),
    ("is_white_checkmate", "?"),
    ("is_black_checkmate", "?"),
    ("is_draw", "?"),
]
ACTION_DTYPE = [
    ("src", "<u8"),
    ("dst", "<u8"),
    ("action_flag", "<i8"),
]
cdef int BLACK = 0
cdef int WHITE = 1
cdef int MAX_PLY = 5000
cdef Bitboard EMPTY = 0
cdef int BLACK_ROOK = 0
cdef int BLACK_KNIGHT = 1
cdef int BLACK_BISHOP = 2
cdef int BLACK_QUEEN = 3
cdef int BLACK_KING = 4
cdef int BLACK_PAWN = 5
cdef int WHITE_ROOK = 6
cdef int WHITE_KNIGHT = 7
cdef int WHITE_BISHOP = 8
cdef int WHITE_QUEEN = 9
cdef int WHITE_KING = 10
cdef int WHITE_PAWN = 11
cdef int[12] PIECES = [
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
]
cdef Bitboard A8 = 1 << 0
cdef Bitboard B8 = 1 << 1
cdef Bitboard C8 = 1 << 2
cdef Bitboard D8 = 1 << 3
cdef Bitboard E8 = 1 << 4
cdef Bitboard F8 = 1 << 5
cdef Bitboard G8 = 1 << 6
cdef Bitboard H8 = 1 << 7
cdef Bitboard A7 = 1 << 8
cdef Bitboard B7 = 1 << 9
cdef Bitboard C7 = 1 << 10
cdef Bitboard D7 = 1 << 11
cdef Bitboard E7 = 1 << 12
cdef Bitboard F7 = 1 << 13
cdef Bitboard G7 = 1 << 14
cdef Bitboard H7 = 1 << 15
cdef Bitboard A6 = 1 << 16
cdef Bitboard B6 = 1 << 17
cdef Bitboard C6 = 1 << 18
cdef Bitboard D6 = 1 << 19
cdef Bitboard E6 = 1 << 20
cdef Bitboard F6 = 1 << 21
cdef Bitboard G6 = 1 << 22
cdef Bitboard H6 = 1 << 23
cdef Bitboard A5 = 1 << 24
cdef Bitboard B5 = 1 << 25
cdef Bitboard C5 = 1 << 26
cdef Bitboard D5 = 1 << 27
cdef Bitboard E5 = 1 << 28
cdef Bitboard F5 = 1 << 29
cdef Bitboard G5 = 1 << 30
cdef Bitboard H5 = 1 << 31
cdef Bitboard A4 = 1 << 32
cdef Bitboard B4 = 1 << 33
cdef Bitboard C4 = 1 << 34
cdef Bitboard D4 = 1 << 35
cdef Bitboard E4 = 1 << 36
cdef Bitboard F4 = 1 << 37
cdef Bitboard G4 = 1 << 38
cdef Bitboard H4 = 1 << 39
cdef Bitboard A3 = 1 << 40
cdef Bitboard B3 = 1 << 41
cdef Bitboard C3 = 1 << 42
cdef Bitboard D3 = 1 << 43
cdef Bitboard E3 = 1 << 44
cdef Bitboard F3 = 1 << 45
cdef Bitboard G3 = 1 << 46
cdef Bitboard H3 = 1 << 47
cdef Bitboard A2 = 1 << 48
cdef Bitboard B2 = 1 << 49
cdef Bitboard C2 = 1 << 50
cdef Bitboard D2 = 1 << 51
cdef Bitboard E2 = 1 << 52
cdef Bitboard F2 = 1 << 53
cdef Bitboard G2 = 1 << 54
cdef Bitboard H2 = 1 << 55
cdef Bitboard A1 = 1 << 56
cdef Bitboard B1 = 1 << 57
cdef Bitboard C1 = 1 << 58
cdef Bitboard D1 = 1 << 59
cdef Bitboard E1 = 1 << 60
cdef Bitboard F1 = 1 << 61
cdef Bitboard G1 = 1 << 62
cdef Bitboard H1 = 1 << 63
cdef Bitboard[8][8] IJ_TO_BB = [
#     1   2   3   4   5   6   7   8    j/i
    [A8, B8, C8, D8, E8, F8, G8, H8], #  1  
    [A7, B7, C7, D7, E7, F7, G7, H7], #  2
    [A6, B6, C6, D6, E6, F6, G6, H6], #  3
    [A5, B5, C5, D5, E5, F5, G5, H5], #  4
    [A4, B4, C4, D4, E4, F4, G4, H4], #  5
    [A3, B3, C3, D3, E3, F3, G3, H3], #  6
    [A2, B2, C2, D2, E2, F2, G2, H2], #  7
    [A1, B1, C1, D1, E1, F1, G1, H1], #  8
]
BB_TO_IJ = {
    IJ_TO_BB[i][j]: (i, j)
    for i in range(8)
    for j in range(8)
}
cdef Bitboard RANK_8 = A8 | B8 | C8 | D8 | E8 | F8 | G8 | H8
cdef Bitboard RANK_7 = A7 | B7 | C7 | D7 | E7 | F7 | G7 | H7
cdef Bitboard RANK_6 = A6 | B6 | C6 | D6 | E6 | F6 | G6 | H6
cdef Bitboard RANK_5 = A5 | B5 | C5 | D5 | E5 | F5 | G5 | H5
cdef Bitboard RANK_4 = A4 | B4 | C4 | D4 | E4 | F4 | G4 | H4
cdef Bitboard RANK_3 = A3 | B3 | C3 | D3 | E3 | F3 | G3 | H3
cdef Bitboard RANK_2 = A2 | B2 | C2 | D2 | E2 | F2 | G2 | H2
cdef Bitboard RANK_1 = A1 | B1 | C1 | D1 | E1 | F1 | G1 | H1
cdef Bitboard FILE_H = H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8
cdef Bitboard FILE_G = G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8
cdef Bitboard FILE_F = F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8
cdef Bitboard FILE_E = E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8
cdef Bitboard FILE_D = D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8
cdef Bitboard FILE_C = C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8
cdef Bitboard FILE_B = B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8
cdef Bitboard FILE_A = A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8
# The magic lookups are taken from the very awesome GunshipPenguin/shallow-blue Github project. See:
#    MAGIC_ROOK: https://github.com/GunshipPenguin/shallow-blue/blob/c6d7e9615514a86533a9e0ffddfc96e058fc9cfd/src/attacks.h#L120
#    MAGIC_BISHOP: https://github.com/GunshipPenguin/shallow-blue/blob/c6d7e9615514a86533a9e0ffddfc96e058fc9cfd/src/attacks.h#L136
# For a nice explanation one can read: https://rhysre.net/fast-chess-move-generation-with-magic-bitboards.html
cdef Bitboard[64] MAGIC_ROOK = [
    0xa8002c000108020, 0x6c00049b0002001, 0x100200010090040, 0x2480041000800801, 0x280028004000800,
    0x900410008040022, 0x280020001001080, 0x2880002041000080, 0xa000800080400034, 0x4808020004000,
    0x2290802004801000, 0x411000d00100020, 0x402800800040080, 0xb000401004208, 0x2409000100040200,
    0x1002100004082, 0x22878001e24000, 0x1090810021004010, 0x801030040200012, 0x500808008001000,
    0xa08018014000880, 0x8000808004000200, 0x201008080010200, 0x801020000441091, 0x800080204005,
    0x1040200040100048, 0x120200402082, 0xd14880480100080, 0x12040280080080, 0x100040080020080,
    0x9020010080800200, 0x813241200148449, 0x491604001800080, 0x100401000402001, 0x4820010021001040,
    0x400402202000812, 0x209009005000802, 0x810800601800400, 0x4301083214000150, 0x204026458e001401,
    0x40204000808000, 0x8001008040010020, 0x8410820820420010, 0x1003001000090020, 0x804040008008080,
    0x12000810020004, 0x1000100200040208, 0x430000a044020001, 0x280009023410300, 0xe0100040002240,
    0x200100401700, 0x2244100408008080, 0x8000400801980, 0x2000810040200, 0x8010100228810400,
    0x2000009044210200, 0x4080008040102101, 0x40002080411d01, 0x2005524060000901, 0x502001008400422,
    0x489a000810200402, 0x1004400080a13, 0x4000011008020084, 0x26002114058042
]
cdef Bitboard[64] MAGIC_BISHOP = [
    0x89a1121896040240, 0x2004844802002010, 0x2068080051921000, 0x62880a0220200808, 0x4042004000000,
    0x100822020200011, 0xc00444222012000a, 0x28808801216001, 0x400492088408100, 0x201c401040c0084,
    0x840800910a0010, 0x82080240060, 0x2000840504006000, 0x30010c4108405004, 0x1008005410080802,
    0x8144042209100900, 0x208081020014400, 0x4800201208ca00, 0xf18140408012008, 0x1004002802102001,
    0x841000820080811, 0x40200200a42008, 0x800054042000, 0x88010400410c9000, 0x520040470104290,
    0x1004040051500081, 0x2002081833080021, 0x400c00c010142, 0x941408200c002000, 0x658810000806011,
    0x188071040440a00, 0x4800404002011c00, 0x104442040404200, 0x511080202091021, 0x4022401120400,
    0x80c0040400080120, 0x8040010040820802, 0x480810700020090, 0x102008e00040242, 0x809005202050100,
    0x8002024220104080, 0x431008804142000, 0x19001802081400, 0x200014208040080, 0x3308082008200100,
    0x41010500040c020, 0x4012020c04210308, 0x208220a202004080, 0x111040120082000, 0x6803040141280a00,
    0x2101004202410000, 0x8200000041108022, 0x21082088000, 0x2410204010040, 0x40100400809000,
    0x822088220820214, 0x40808090012004, 0x910224040218c9, 0x402814422015008, 0x90014004842410,
    0x1000042304105, 0x10008830412a00, 0x2520081090008908, 0x40102000a0a60140,
]
cdef Bitboard NO_MOVE = 0


cdef Bitboard ij_to_bb(int i, int j):
    cdef Bitboard cursor = 1
    for i_ in range(8):
        for j_ in range(8):
            if i == i_ and j == j_:
                return cursor
            cursor = cursor << 1


cdef bint inside_board(long i, long j):
    return 0 <= i <= 7 and 0 <= j <= 7


cdef int pop_count(Bitboard x):
    cdef int i
    count = 0
    for i in range(64):
        count += x & 1
        x >>= 1
    return count


cdef Bitboard blockers(int blocker_idx, Bitboard b):
    cdef int i
    cdef Bitboard blockers = 0
    bits = pop_count(b)
    for i in range(bits):
        bit_index = (b&-b).bit_length()-1
        if blocker_idx & (1 << i):
            blockers |= (1 << bit_index)
        b &= b - 1
    return blockers


def bb_to_ijs(bb):
    ijs = []
    for i in range(8):
        for j in range(8):
            if np.uint64(ij_to_bb(i, j)) & np.uint64(bb):
                ijs.append((i, j))
    return ijs


def bb_to_ij(bb):
    ijs = bb_to_ijs(bb)
    assert len(ijs) == 1
    return ijs[0]


cdef class Environment:
    # A stateless environment with two main public methods: actions(state) and step(state, action).
    cdef readonly cpp_map[Bitboard, Bitboard] _king_attackset_lookup
    cdef readonly cpp_map[Bitboard, Bitboard] _knight_attackset_lookup
    
    cdef readonly cpp_map[Bitboard, Bitboard] _rook_to_magic_lookup
    cdef readonly cpp_map[Bitboard, Bitboard] _rook_magic_shifts_lookup
    cdef readonly cpp_map[Bitboard, Bitboard] _rook_blockermask_lookup
    cdef readonly cpp_map[Bitboard, cpp_map[Bitboard, Bitboard]] _rook_table_lookup
    
    cdef readonly cpp_map[Bitboard, Bitboard] _bishop_to_magic_lookup
    cdef readonly cpp_map[Bitboard, Bitboard] _bishop_magic_shifts_lookup
    cdef readonly cpp_map[Bitboard, Bitboard] _bishop_blockermask_lookup
    cdef readonly cpp_map[Bitboard, cpp_map[Bitboard, Bitboard]] _bishop_table_lookup

    def __init__(self):
        self._init_king_attackset_lookup()
        self._init_knight_attackset_lookup()
        
        self._init_rook_to_magic_lookup()
        self._init_rook_magic_shifts_lookup()
        self._init_rook_blockermask_lookup()
        self._init_rook_table_lookup()

        self._init_bishop_to_magic_lookup()
        self._init_bishop_magic_shifts_lookup()
        self._init_bishop_blockermask_lookup()
        self._init_bishop_table_lookup()

    def actions(self, state):
        if isinstance(state, np.void):
            return self._actions(state)
        elif isinstance(state, np.ndarray):
            if state.shape[0] > 1:
                raise ValueError()
            return self._actions(state[0])
        else:
            raise NotImplementedError()
    
    cdef _actions(self, State state):
        cdef cnp.ndarray[Action, ndim=1] actions_array
        cdef cnp.ndarray[State, ndim=1] next_state
        actions_array = self._pseudo_actions(state)
        next_state = self._step(state, actions_array, _step_ahead=False)
        if state.white_player_turn:
            return actions_array[~next_state["is_white_check"]]
        else:
            return actions_array[~next_state["is_black_check"]]
    
    def pseudo_actions(self, state):
        if isinstance(state, np.void):
            return self._pseudo_actions(state)
        elif isinstance(state, np.ndarray):
            if state.shape[0] > 1:
                raise ValueError()
            return self._pseudo_actions(state[0])
        else:
            raise NotImplementedError()
            
    cdef _pseudo_actions(self, State state):
        cdef Bitboard color, other_color, occupied, other_attackset
        cdef cpp_vector[Action] action_vector = []
        
        if state.white_player_turn:
            
            color = state.white_rook | state.white_knight | state.white_bishop | state.white_queen | state.white_king | state.white_pawn
            other_color = state.black_rook | state.black_knight | state.black_bishop | state.black_queen | state.black_king | state.black_pawn
            occupied = color | other_color
            other_attackset = (
                self.king_attackset(state.black_king)
                | self.rook_attackset(state.black_rook | state.black_queen, occupied)
                | self.knight_attackset(state.black_knight)
                | self.bishop_attackset(state.black_bishop | state.black_queen, occupied)
                | self.black_pawn_attackset(state.black_pawn)
            )
            
            self._king_actions(action_vector, state.white_king, color, other_attackset, ActionFlag.move_white_king)
            self._knight_actions(action_vector, state.white_knight, color, ActionFlag.move_white_knight)
            self._rook_actions(action_vector, state.white_rook, occupied, color, ActionFlag.move_white_rook)
            self._bishop_actions(action_vector, state.white_bishop, occupied, color, ActionFlag.move_white_bishop)
            self._queen_actions(action_vector, state.white_queen, occupied, color, ActionFlag.move_white_queen)
            self._white_pawn_actions(action_vector, state.white_pawn, occupied, other_color, state.en_passant_square_white)
            self._white_rook_queenside_castling_actions(action_vector, state.white_rook, state.white_king, occupied, state.has_white_king_moved, state.has_white_queenside_rook_moved)
            self._white_rook_kingside_castling_actions(action_vector, state.white_rook, state.white_king, occupied, state.has_white_king_moved, state.has_white_kingside_rook_moved)
        
        else:
            
            color = state.black_rook | state.black_knight | state.black_bishop | state.black_queen | state.black_king | state.black_pawn
            other_color = state.white_rook | state.white_knight | state.white_bishop | state.white_queen | state.white_king | state.white_pawn
            occupied = color | other_color
            other_attackset = (
                self.king_attackset(state.white_king)
                | self.rook_attackset(state.white_rook | state.white_queen, occupied)
                | self.knight_attackset(state.white_knight)
                | self.bishop_attackset(state.white_bishop | state.white_queen, occupied)
                | self.white_pawn_attackset(state.white_pawn)
            )
    
            self._king_actions(action_vector, state.black_king, color, other_attackset, ActionFlag.move_black_king)
            self._knight_actions(action_vector, state.black_knight, color, ActionFlag.move_black_knight)
            self._rook_actions(action_vector, state.black_rook, occupied, color, ActionFlag.move_black_rook)
            self._bishop_actions(action_vector, state.black_bishop, occupied, color, ActionFlag.move_black_bishop)
            self._queen_actions(action_vector, state.black_queen, occupied, color, ActionFlag.move_black_queen)
            self._black_pawn_actions(action_vector, state.black_pawn, occupied, other_color, state.en_passant_square_black)
            self._black_rook_queenside_castling_actions(action_vector, state.black_rook, state.black_king, occupied, state.has_black_king_moved, state.has_black_queenside_rook_moved)
            self._black_rook_kingside_castling_actions(action_vector, state.black_rook, state.black_king, occupied, state.has_black_king_moved, state.has_black_kingside_rook_moved)
            
        if action_vector.size() == 0:
            return np.array([], dtype=ACTION_DTYPE)
    
        # Cast memoryview of cpp vector to numpy array
        cdef Action [::1] actions_view = <Action [:action_vector.size()]>action_vector.data()
        cdef cnp.ndarray[Action, ndim=1] actions_array = np.asarray(actions_view, dtype=ACTION_DTYPE)
        return actions_array
    
    def step(self, state, action):
        if isinstance(action, np.void):
            action = np.asarray(action, dtype=ACTION_DTYPE).reshape(-1)
        if isinstance(state, np.void):
            return self._step(state, action, _step_ahead=True)
        elif isinstance(state, np.ndarray):
            if state.shape[0] > 1:
                raise ValueError()
            return self._step(state[0], action, _step_ahead=True)
        else:
            raise NotImplementedError()
    
    cdef _step(self, State state, const Action [:] action, cnp.npy_bool _step_ahead=True):
        cdef int i
        cdef cnp.ndarray[State, ndim=1] new_state = np.empty(action.shape[0], dtype=STATE_DTYPE)
        cdef State [:] new_state_view = new_state
        for i in range(action.shape[0]):
            new_state_view[i] = self._step_scalar(state, action[i], _step_ahead)
        return new_state
    
    cdef _step_scalar(self, State state, Action action, cnp.npy_bool _step_ahead):
        
        # change color
        state.white_player_turn = not state.white_player_turn

        # remove piece at dst 
        state.black_rook = state.black_rook & ~action.dst
        state.black_knight = state.black_knight & ~action.dst
        state.black_bishop = state.black_bishop & ~action.dst
        state.black_queen = state.black_queen & ~action.dst
        state.black_king = state.black_king & ~action.dst
        state.black_pawn = state.black_pawn & ~action.dst
        state.white_rook = state.white_rook & ~action.dst
        state.white_knight = state.white_knight & ~action.dst
        state.white_bishop = state.white_bishop & ~action.dst
        state.white_queen = state.white_queen & ~action.dst
        state.white_king = state.white_king & ~action.dst
        state.white_pawn = state.white_pawn & ~action.dst
        
        # reset
        state.en_passant_square_black = EMPTY
        state.en_passant_square_white = EMPTY
    
        if action.flag == ActionFlag.move_black_rook:
            state.black_rook = state.black_rook & ~action.src | action.dst
            if action.src & A8:
                state.has_black_queenside_rook_moved = True
            if action.src & H8:
                state.has_black_kingside_rook_moved = True
        elif action.flag == ActionFlag.move_black_knight:
            state.black_knight = state.black_knight & ~action.src | action.dst
        elif action.flag == ActionFlag.move_black_bishop:
            state.black_bishop = state.black_bishop & ~action.src | action.dst
        elif action.flag == ActionFlag.move_black_queen:
            state.black_queen = state.black_queen & ~action.src | action.dst
        elif action.flag == ActionFlag.move_black_king:
            state.black_king = state.black_king & ~action.src | action.dst
            state.has_black_king_moved = True
        elif action.flag == ActionFlag.move_black_pawn:
            state.black_pawn = state.black_pawn & ~action.src | action.dst
        elif action.flag == ActionFlag.move_black_pawn_double:
            state.black_pawn = state.black_pawn & ~action.src | action.dst
            if action.dst & FILE_A:
                state.en_passant_square_white = A6
            elif action.dst & FILE_B:
                state.en_passant_square_white = B6
            elif action.dst & FILE_C:
                state.en_passant_square_white = C6
            elif action.dst & FILE_D:
                state.en_passant_square_white = D6
            elif action.dst & FILE_E:
                state.en_passant_square_white = E6
            elif action.dst & FILE_F:
                state.en_passant_square_white = F6
            elif action.dst & FILE_G:
                state.en_passant_square_white = G6
            elif action.dst & FILE_H:
                state.en_passant_square_white = H6
            else:
                raise NotImplementedError()
        elif action.flag == ActionFlag.move_white_rook:
            state.white_rook = state.white_rook & ~action.src | action.dst
            if action.src & A1:
                state.has_white_queenside_rook_moved = True
            if action.src & H1:
                state.has_white_kingside_rook_moved = True
        elif action.flag == ActionFlag.move_white_knight:
            state.white_knight = state.white_knight & ~action.src | action.dst
        elif action.flag == ActionFlag.move_white_bishop:
            state.white_bishop = state.white_bishop & ~action.src | action.dst
        elif action.flag == ActionFlag.move_white_queen:
            state.white_queen = state.white_queen & ~action.src | action.dst
        elif action.flag == ActionFlag.move_white_king:
            state.white_king = state.white_king & ~action.src | action.dst
            state.has_white_king_moved = True
        elif action.flag == ActionFlag.move_white_pawn:
            state.white_pawn = state.white_pawn & ~action.src | action.dst
        elif action.flag == ActionFlag.move_white_pawn_double:
            state.white_pawn = state.white_pawn & ~action.src | action.dst
            if action.dst & FILE_A:
                state.en_passant_square_black = A3
            elif action.dst & FILE_B:
                state.en_passant_square_black = B3
            elif action.dst & FILE_C:
                state.en_passant_square_black = C3
            elif action.dst & FILE_D:
                state.en_passant_square_black = D3
            elif action.dst & FILE_E:
                state.en_passant_square_black = E3
            elif action.dst & FILE_F:
                state.en_passant_square_black = F3
            elif action.dst & FILE_G:
                state.en_passant_square_black = G3
            elif action.dst & FILE_H:
                state.en_passant_square_black = H3
            else:
                raise NotImplementedError()
        elif action.flag == ActionFlag.castle_queenside_black:
            state.black_rook = (state.black_rook & ~A8) | D8
            state.black_king = C8
            state.has_black_king_moved = True
            state.has_black_queenside_rook_moved = True
        elif action.flag == ActionFlag.castle_kingside_black:
            state.black_rook = (state.black_rook & ~H8) | F8
            state.black_king = G8
            state.has_black_king_moved = True
            state.has_black_kingside_rook_moved = True
        elif action.flag == ActionFlag.castle_queenside_white:
            state.white_rook = (state.white_rook & ~A1) | D1
            state.white_king = C1
            state.has_white_king_moved = True
            state.has_white_queenside_rook_moved = True
        elif action.flag == ActionFlag.castle_kingside_white:
            state.white_rook = (state.white_rook & ~H1) | F1
            state.white_king = G1
            state.has_white_king_moved = True
            state.has_white_kingside_rook_moved = True
        elif action.flag == ActionFlag.promote_black_rook:
            state.black_pawn = state.black_pawn & ~action.src
            state.black_rook = state.black_rook | action.src
        elif action.flag == ActionFlag.promote_black_knight:
            state.black_pawn = state.black_pawn & ~action.src
            state.black_knight = state.black_knight | action.src
        elif action.flag == ActionFlag.promote_black_bishop:
            state.black_pawn = state.black_pawn & ~action.src
            state.black_bishop = state.black_bishop | action.src
        elif action.flag == ActionFlag.promote_black_queen:
            state.black_pawn = state.black_pawn & ~action.src
            state.black_queen = state.black_queen | action.src
        elif action.flag == ActionFlag.promote_black_pawn:
            state.black_pawn = state.black_pawn & ~action.src
            state.black_pawn = state.black_pawn | action.src
        elif action.flag == ActionFlag.promote_white_rook:
            state.white_pawn = state.white_pawn & ~action.src
            state.white_rook = state.white_rook | action.src
        elif action.flag == ActionFlag.promote_white_knight:
            state.white_pawn = state.white_pawn & ~action.src
            state.white_knight = state.white_knight | action.src
        elif action.flag == ActionFlag.promote_white_bishop:
            state.white_pawn = state.white_pawn & ~action.src
            state.white_bishop = state.white_bishop | action.src
        elif action.flag == ActionFlag.promote_white_queen:
            state.white_pawn = state.white_pawn & ~action.src
            state.white_queen = state.white_queen | action.src
        elif action.flag == ActionFlag.promote_white_pawn:
            state.white_pawn = state.white_pawn & ~action.src
            state.white_pawn = state.white_pawn | action.src
        elif action.flag == ActionFlag.move_black_pawn_en_passant:
            state.black_pawn = state.black_pawn & ~action.src | action.dst
        elif action.flag == ActionFlag.move_white_pawn_en_passant:
            state.white_pawn = state.white_pawn & ~action.src | action.dst
        else:
            raise NotImplementedError()
    
        state.ply = state.ply + 1
        state.is_black_check = self._is_black_check(state)
        state.is_white_check = self._is_white_check(state)
        
    
        # Simulate one step ahead, _step_ahead=False to avoid infinite recursion
        if _step_ahead:
            next_pseudo_states = self._step(state, self._pseudo_actions(state), _step_ahead=False)
            if state.is_black_check:
                state.is_black_checkmate = next_pseudo_states["is_black_check"].all()
            if state.is_white_check:
                state.is_white_checkmate = next_pseudo_states["is_white_check"].all()
            state.is_draw = self._is_draw(state, next_pseudo_states)
            
        return state

    def is_white_check(self, state):
        return self._is_white_check(state[0])
    
    def is_black_check(self, state):
        return self._is_black_check(state[0])
    
    def is_white_checkmate(self, state):
        next_pseudo_states = self._step(state[0], self._pseudo_actions(state[0]), _step_ahead=False)
        return self._is_white_checkmate(state[0], next_pseudo_states)
    
    def is_black_checkmate(self, state):
        next_pseudo_states = self._step(state[0], self._pseudo_actions(state[0]), _step_ahead=False)
        return self._is_black_checkmate(state[0], next_pseudo_states)
    
    cdef bint _is_white_check(self, State state):
        cdef Bitboard color, other_color, occupied, other_attackset
        color = state.white_rook | state.white_knight | state.white_bishop | state.white_queen | state.white_king | state.white_pawn
        other_color = state.black_rook | state.black_knight | state.black_bishop | state.black_queen | state.black_king | state.black_pawn
        occupied = color | other_color
        other_attackset = (
            self.rook_attackset(state.black_rook | state.black_queen, occupied)
            | self.knight_attackset(state.black_knight)
            | self.bishop_attackset(state.black_bishop | state.black_queen, occupied)
            | self.black_pawn_attackset(state.black_pawn)
        )
        if other_attackset & state.white_king:
            return True
        return False
    
    cdef bint _is_black_check(self, State state):
        cdef Bitboard color, other_color, occupied, other_attackset
        color = state.black_rook | state.black_knight | state.black_bishop | state.black_queen | state.black_king | state.black_pawn
        other_color = state.white_rook | state.white_knight | state.white_bishop | state.white_queen | state.white_king | state.white_pawn
        occupied = color | other_color
        other_attackset = (
            self.rook_attackset(state.white_rook | state.white_queen, occupied)
            | self.knight_attackset(state.white_knight)
            | self.bishop_attackset(state.white_bishop | state.white_queen, occupied)
            | self.white_pawn_attackset(state.white_pawn)
        )
        if other_attackset & state.black_king:
            return True
        return False
    
    cdef bint _is_draw(self, State state, cnp.ndarray[State, ndim=1] next_pseudo_states):
        return (
            (state.ply >= MAX_PLY)
            or self._insufficient_material_king_vs_king(state)
            or self._is_stalemate(state, next_pseudo_states)
        )
    
    cdef bint _is_white_checkmate(self, State state, cnp.ndarray[State, ndim=1] next_pseudo_states):
        if self._is_white_check(state):
            return next_pseudo_states["is_white_check"].all()
        return False
    
    cdef bint _is_black_checkmate(self, State state, cnp.ndarray[State, ndim=1] next_pseudo_states):
        if self._is_black_check(state):
            return next_pseudo_states["is_black_check"].all()
        return False
    
    cdef bint _insufficient_material_king_vs_king(self, State state):
        return (
            state.black_rook
            | state.black_knight
            | state.black_bishop
            | state.black_queen
            | state.black_pawn
            | state.white_rook
            | state.white_knight
            | state.white_bishop
            | state.white_queen 
            | state.white_pawn
        ) == EMPTY
    
    cdef bint _is_stalemate(self, State state, cnp.ndarray[State, ndim=1] next_pseudo_states):
        if state.white_player_turn:    
            return not state.is_white_check and next_pseudo_states["is_white_check"].all()
        else:
            return not state.is_black_check and next_pseudo_states["is_black_check"].all()

    cdef Bitboard king_attackset(self, Bitboard king):
        return self._king_attackset_lookup[king]

    cdef Bitboard knight_attackset(self, Bitboard knight):
        attackset = 0
        while knight:
            src = knight & -knight
            attackset |= self._knight_attackset_lookup[src]
            knight &= knight - 1
        return attackset

    cpdef Bitboard rook_attackset_slow(self, int i, int j, Bitboard blockers):
        cdef int step
        cdef Bitboard attackset = 0
        blocker_pos = bb_to_ijs(blockers)
    
        for step in range(1, i + 1):
            attackset |= ij_to_bb(i - step, j)
            if (i - step, j) in blocker_pos:
                break
    
        for step in range(1, 8 - i):
            attackset |= ij_to_bb(i + step, j)
            if (i + step, j) in blocker_pos:
                break
    
        for step in range(1, j + 1):
            attackset |= ij_to_bb(i, j - step)
            if (i, j - step) in blocker_pos:
                break
    
        for step in range(1, 8 - j):
            attackset |= ij_to_bb(i, j + step)
            if (i, j + step) in blocker_pos:
                break
    
        return attackset

    cpdef rook_attackset(self, Bitboard rook, Bitboard blockers):
        cdef Bitboard src, dst, attackset
        cdef int key
        attackset = 0
        if rook == EMPTY:
            return attackset
        while rook:
            src = rook & -rook
            key = self.rook_key(src, blockers & self.rook_blockermask(src))
            attackset |= self.rook_table(src, key)
            rook &= rook - 1
        return attackset

    cpdef bishop_attackset_slow(self, int i, int j, Bitboard blockers):
        cdef int step
        cdef Bitboard attackset = 0
        blocker_pos = bb_to_ijs(blockers)
    
        for step in range(1, min(8 - i, 8 - j)):
            attackset |= ij_to_bb(i + step, j + step)
            if (i + step, j + step) in blocker_pos:
                break
    
        for step in range(1, min(i + 1, 8 - j)):
            attackset |= ij_to_bb(i - step, j + step)
            if (i - step, j + step) in blocker_pos:
                break
    
        for step in range(1, min(i + 1, j + 1)):
            attackset |= ij_to_bb(i - step, j - step)
            if (i - step, j - step) in blocker_pos:
                break
    
        for step in range(1, min(8 - i, j + 1)):
            attackset |= ij_to_bb(i + step, j - step)
            if (i + step, j - step) in blocker_pos:
                break
    
        return attackset

    cpdef Bitboard bishop_attackset(self, Bitboard bishop, Bitboard blockers):
        cdef Bitboard src, dst, attackset
        cdef int key
        attackset = 0
        if bishop == EMPTY:
            return attackset
        while bishop:
            src = bishop & -bishop
            key = self.bishop_key(src, blockers & self.bishop_blockermask(src))
            attackset |= self.bishop_table(src, key)
            bishop &= bishop - 1
        return attackset

    cdef Bitboard rook_to_magic(self, Bitboard rook):
        return self._rook_to_magic_lookup[rook]    
    
    cdef Bitboard rook_magic_shifts(self, Bitboard rook):
        return self._rook_magic_shifts_lookup[rook]
    
    cdef Bitboard rook_blockermask(self, Bitboard rook):
        return self._rook_blockermask_lookup[rook]
    
    cdef Bitboard rook_key(self, Bitboard b, Bitboard blockers):
        return (blockers * self.rook_to_magic(b)) >> (64 - self.rook_magic_shifts(b))
    
    cdef Bitboard rook_table(self, Bitboard rook, Bitboard key):
        return self._rook_table_lookup[rook][key]

    cdef Bitboard bishop_to_magic(self, Bitboard bishop):
        return self._bishop_to_magic_lookup[bishop]
    
    cdef Bitboard bishop_magic_shifts(self, Bitboard bishop):
        return self._bishop_magic_shifts_lookup[bishop]
    
    cdef Bitboard bishop_blockermask(self, Bitboard bishop):
        return self._bishop_blockermask_lookup[bishop]
    
    cdef Bitboard bishop_key(self, Bitboard b, Bitboard blockers):
        return (blockers * self.bishop_to_magic(b)) >> (64 - self.bishop_magic_shifts(b))
    
    cdef Bitboard bishop_table(self, Bitboard bishop, int key):
        return self._bishop_table_lookup[bishop][key]

    cdef void _king_actions(self, cpp_vector[Action]& action_vector, Bitboard king, Bitboard color, Bitboard other_attackset, int flag):
        cdef Bitboard dst, attackset 
        attackset = self.king_attackset(king) & ~color & ~other_attackset
        while attackset:
            dst = attackset & -attackset
            action_vector.push_back(Action(src=king, dst=dst, flag=flag))
            attackset = attackset & (attackset - 1)
    
    cdef void _knight_actions(self, cpp_vector[Action]& action_vector, Bitboard knight, Bitboard color, int flag):
        cdef Bitboard src, dst, attackset
        while knight:
            src = knight & -knight
            attackset = self.knight_attackset(src) & ~color
            while attackset:
                dst = attackset & -attackset
                action_vector.push_back(Action(src=src, dst=dst, flag=flag))
                attackset = attackset & (attackset - 1)
            knight &= knight - 1

    cdef void _rook_actions(self, cpp_vector[Action]& action_vector, Bitboard rook, Bitboard blockers, Bitboard color, int flag):
        cdef Bitboard src, dst, attackset
        cdef int key
        while rook:
            src = rook & -rook
            key = self.rook_key(src, blockers & self.rook_blockermask(src))
            attackset = self.rook_table(src, key) & ~color
            while attackset:
                dst = attackset & -attackset
                action_vector.push_back(Action(src=src, dst=dst, flag=flag))
                attackset = attackset & (attackset - 1)
            rook &= rook - 1

    cdef void _bishop_actions(self, cpp_vector[Action]& action_vector, Bitboard bishop, Bitboard blockers, Bitboard color, int flag):
        cdef Bitboard src, dst, attackset
        cdef int key
        while bishop:
            src = bishop & -bishop
            key = self.bishop_key(src, blockers & self.bishop_blockermask(src))
            attackset = self.bishop_table(src, key) & ~color
            while attackset:
                dst = attackset & -attackset
                action_vector.push_back(Action(src=src, dst=dst, flag=flag))
                attackset = attackset & (attackset - 1)
            bishop &= bishop - 1
    
    cdef void _queen_actions(self, cpp_vector[Action]& action_vector, Bitboard queen, Bitboard blockers, Bitboard color, int flag):
        self._rook_actions(action_vector, queen, blockers, color, flag)
        self._bishop_actions(action_vector, queen, blockers, color, flag)

    cdef Bitboard white_pawn_attackset(self, Bitboard pawn):
        cdef Bitboard northeastone, northwestone
        northeastone = ((pawn & ~FILE_H) >> 7)
        northwestone = ((pawn & ~FILE_A) >> 9)
        return northwestone | northeastone
    
    cdef Bitboard black_pawn_attackset(self, Bitboard pawn):
        cdef Bitboard southeastone, southwestone
        southeastone = ((pawn & ~FILE_H) << 9)
        southwestone = ((pawn & ~FILE_A) << 7)
        return southwestone | southeastone
    
    cdef void _white_pawn_actions(self, cpp_vector[Action]& action_vector, Bitboard pawn, Bitboard occupied, Bitboard other_color, Bitboard en_passant_square_white):
        cdef Bitboard src, dst, northone, northtwo, attackset
        while pawn:
            src = pawn & -pawn
    
            northone = ((src & ~RANK_8) >> 8) & (~occupied)
            while northone:
                dst = northone & -northone
                if dst & RANK_8:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_rook))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_knight))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_bishop))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_queen))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_pawn))
                else:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_white_pawn))
                northone = northone & (northone - 1)
    
            northtwo = (src >> 16) & (~occupied) & RANK_4
            while northtwo:
                dst = northtwo & -northtwo
                action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_white_pawn_double))
                northtwo = northtwo & (northtwo - 1)
    
            attackset = self.white_pawn_attackset(src) & (other_color | en_passant_square_white)
            while attackset:
                dst = attackset & -attackset
                if dst & en_passant_square_white:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_white_pawn_en_passant))
                elif dst & RANK_8:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_rook))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_knight))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_bishop))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_queen))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_white_pawn))
                else:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_white_pawn))
                attackset = attackset & (attackset - 1)
    
            pawn = pawn & (pawn - 1)
    
    cdef void _black_pawn_actions(self, cpp_vector[Action]& action_vector, Bitboard pawn, Bitboard occupied, Bitboard other_color, Bitboard en_passant_square_black):
        cdef Bitboard src, dst, southone, southtwo, attackset
        while pawn:
            src = pawn & -pawn
    
            southone = ((src & ~RANK_1) << 8) & (~occupied)
            while southone:
                dst = southone & -southone
                if dst & RANK_1:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_rook))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_knight))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_bishop))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_queen))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_pawn))
                else:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_black_pawn))
                southone = southone & (southone - 1)
    
            southtwo = (src << 16) & (~occupied) & RANK_5
            while southtwo:
                dst = southtwo & -southtwo
                action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_black_pawn_double))
                southtwo = southtwo & (southtwo - 1)
    
            attackset = self.black_pawn_attackset(src) & (other_color | en_passant_square_black)
            while attackset:
                dst = attackset & -attackset
                if dst & en_passant_square_black:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_black_pawn_en_passant))
                elif dst & RANK_1:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_rook))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_knight))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_bishop))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_queen))
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.promote_black_pawn))
                else:
                    action_vector.push_back(Action(src=src, dst=dst, flag=ActionFlag.move_black_pawn))
                attackset = attackset & (attackset - 1)
    
            pawn = pawn & (pawn - 1)

    cdef void _black_rook_queenside_castling_actions(
        self,
        cpp_vector[Action]& action_vector,
        Bitboard rook,
        Bitboard king,
        Bitboard occupied,
        cnp.npy_bool has_black_king_moved,
        cnp.npy_bool has_black_queenside_rook_moved,
    ):
        if not (
            (has_black_king_moved or has_black_queenside_rook_moved)
            or (occupied & (B8 | C8 | D8))
            or (not rook & A8)
            or (not king & E8)  # Redundant check, but nice for tests
        ):
            action_vector.push_back(Action(src=NO_MOVE, dst=NO_MOVE, flag=ActionFlag.castle_queenside_black))
    
    cdef void _white_rook_queenside_castling_actions(
        self,
        cpp_vector[Action]& action_vector,
        Bitboard rook,
        Bitboard king,
        Bitboard occupied,
        cnp.npy_bool has_white_king_moved,
        cnp.npy_bool has_white_queenside_rook_moved,
    ):
        if not (
            (has_white_king_moved or has_white_queenside_rook_moved)
            or (occupied & (B1 | C2 | D3))
            or (not rook & A1)
            or (not king & E1)  # Redundant check, but nice for tests
        ):
            action_vector.push_back(Action(src=NO_MOVE, dst=NO_MOVE, flag=ActionFlag.castle_queenside_white))
    
    cdef void _black_rook_kingside_castling_actions(
        self,
        cpp_vector[Action]& action_vector,
        Bitboard rook,
        Bitboard king,
        Bitboard occupied,
        cnp.npy_bool has_black_king_moved,
        cnp.npy_bool has_black_kingside_rook_moved,
    ):
        if not (
            (has_black_kingside_rook_moved or has_black_kingside_rook_moved)
            or (occupied & (F8 | G8))
            or (not rook & H8)
            or (not king & E8)  # Redundant check, but nice for tests
        ):
            action_vector.push_back(Action(src=NO_MOVE, dst=NO_MOVE, flag=ActionFlag.castle_kingside_black))
    
    cdef void _white_rook_kingside_castling_actions(
        self,
        cpp_vector[Action]& action_vector,
        Bitboard rook,
        Bitboard king,
        Bitboard occupied,
        cnp.npy_bool has_white_king_moved,
        cnp.npy_bool has_white_kingside_rook_moved,
    ):
        if not (
            (has_white_kingside_rook_moved or has_white_kingside_rook_moved)
            or (occupied & (F1 | G1))
            or (not rook & H1)
            or (not king & E1)  # Redundant check, but nice for tests
        ):
            action_vector.push_back(Action(src=NO_MOVE, dst=NO_MOVE, flag=ActionFlag.castle_kingside_white))

    cdef _init_king_attackset_lookup(self):
        cdef int src_i, src_j, di, dj
        for src_i in range(8):
            for src_j in range(8):
                self._king_attackset_lookup[ij_to_bb(src_i, src_j)] = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        dst_i = src_i + di
                        dst_j = src_j + dj
                        if inside_board(dst_i, dst_j):
                            self._king_attackset_lookup[ij_to_bb(src_i, src_j)] |= ij_to_bb(dst_i, dst_j)

    cdef _init_knight_attackset_lookup(self):
        cdef int src_i, src_j, di, dj
        for src_i in range(8):
            for src_j in range(8):
                self._knight_attackset_lookup[ij_to_bb(src_i, src_j)] = 0
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
                    dst_i = src_i + di
                    dst_j = src_j + dj
                    if inside_board(dst_i, dst_j):
                        self._knight_attackset_lookup[ij_to_bb(src_i, src_j)] |= ij_to_bb(dst_i, dst_j)

    cdef _init_rook_to_magic_lookup(self):
        cdef int idx, i, j
        cdef Bitboard bb
        idx = 0
        for i in range(8):
            for j in range(8):    
                bb = ij_to_bb(i, j)
                self._rook_to_magic_lookup[bb] = <Bitboard> MAGIC_ROOK[idx]
                idx += 1

    cdef _init_rook_magic_shifts_lookup(self):
        cdef int i, j
        cdef Bitboard bb
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                self._rook_magic_shifts_lookup[bb] = 0
    
                for step in range(1, i):
                    self._rook_magic_shifts_lookup[bb] += 1
    
                for step in range(1, 7 - i):
                    self._rook_magic_shifts_lookup[bb] += 1
    
                for step in range(1, j):
                    self._rook_magic_shifts_lookup[bb] += 1
    
                for step in range(1, 7 - j):
                    self._rook_magic_shifts_lookup[bb] += 1

    cdef _init_rook_blockermask_lookup(self):
        cdef int i, j, step
        cdef Bitboard bb
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                self._rook_blockermask_lookup[bb] = 0
    
                for step in range(1, i):
                    self._rook_blockermask_lookup[bb] |= ij_to_bb(i - step, j)
    
                for step in range(1, 7 - i):
                    self._rook_blockermask_lookup[bb] |= ij_to_bb(i + step, j)
    
                for step in range(1, j):
                    self._rook_blockermask_lookup[bb] |= ij_to_bb(i, j - step)
    
                for step in range(1, 7 - j):
                    self._rook_blockermask_lookup[bb] |= ij_to_bb(i, j + step)

    cdef _init_rook_table_lookup(self):
        cdef int i, j, blocker_idx
        cdef Bitboard bb, key, blockers_, attackset
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                for blocker_idx in range(0, 1 << self.rook_magic_shifts(bb)):
                    blockers_ = blockers(blocker_idx, self.rook_blockermask(bb))
                    key = self.rook_key(bb, blockers_)
                    attackset = self.rook_attackset_slow(i, j, blockers_)
                    self._rook_table_lookup[bb][key] = attackset

    cdef _init_bishop_to_magic_lookup(self):
        cdef int idx, i, j
        cdef Bitboard bb
        idx = 0
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                self._bishop_to_magic_lookup[bb] = MAGIC_BISHOP[idx]
                idx += 1

    cdef _init_bishop_magic_shifts_lookup(self):
        cdef int i, j, step
        cdef Bitboard bb
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                self._bishop_magic_shifts_lookup[bb] = 0
    
                for step in range(1, min(7 - i, 7 - j)):
                    self._bishop_magic_shifts_lookup[bb] += 1
    
                for step in range(1, min(i, 7 - j)):
                    self._bishop_magic_shifts_lookup[bb] += 1
    
                for step in range(1, min(i, j)):
                    self._bishop_magic_shifts_lookup[bb] += 1
    
                for step in range(1, min(7 - i, j)):
                    self._bishop_magic_shifts_lookup[bb] += 1

    cdef _init_bishop_blockermask_lookup(self):
        cdef int i, j, step
        cdef Bitboard bb
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                self._bishop_blockermask_lookup[bb] = 0
    
                for step in range(1, min(7 - i, 7 - j)):
                    self._bishop_blockermask_lookup[bb] |= ij_to_bb(i + step, j + step)
    
                for step in range(1, min(i, 7 - j)):
                    self._bishop_blockermask_lookup[bb] |= ij_to_bb(i - step, j + step)
    
                for step in range(1, min(i, j)):
                    self._bishop_blockermask_lookup[bb] |= ij_to_bb(i - step, j - step)
    
                for step in range(1, min(7 - i, j)):
                    self._bishop_blockermask_lookup[bb] |= ij_to_bb(i + step, j - step)

    cdef _init_bishop_table_lookup(self):
        cdef int i, j, step, blocker_idx
        cdef Bitboard bb, key, blockers_, attackset
        for i in range(8):
            for j in range(8):
                bb = ij_to_bb(i, j)
                for blocker_idx in range(0, 1 << self.bishop_magic_shifts(bb)):
                    blockers_ = blockers(blocker_idx, self.bishop_blockermask(bb))
                    key = self.bishop_key(bb, blockers_)
                    attackset = self.bishop_attackset_slow(i, j, blockers_)
                    self._bishop_table_lookup[bb][key] = attackset
                


cdef class AlphaBetaSearch:
    cdef Environment _env

    def __init__(self, env):
        self._env = env

    cpdef search(self, State state, int depth, cnp.ndarray[double, ndim=1] piece_value):
        cdef cnp.ndarray[Action, ndim=1] actions = self._env._actions(state)
        cdef cnp.ndarray[double, ndim=1] value_array = np.empty(shape=actions.shape[0], dtype=np.float64)
        for idx in range(actions.shape[0]):
            new_state = self._env._step(state, actions[[idx]])
            value_array[idx] = self._alphabeta(
                state=new_state,
                depth=depth - 1,
                piece_value=piece_value,
                alpha=-np.inf,
                beta=np.inf,
                maximizing_player=False,
            )
        return actions, value_array

    cdef _alphabeta(
        self,
        State state,
        int depth,
        cnp.ndarray[double, ndim=1] piece_value,
        double alpha,
        double beta,
        bint maximizing_player,
    ):
        """Minimax with alpha-beta pruning."""

        if depth == 0:
            value = self.state_value(state, piece_value)
        else:
            actions = self._env._actions(state)
            if maximizing_player:
                value = -np.inf
                for idx in range(actions.shape[0]):
                    new_state = self._env._step(state, actions[[idx]])
                    new_value = self._alphabeta(new_state, depth - 1, piece_value, alpha, beta, False)
                    value = max(value, new_value)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            else:
                value = np.inf
                for idx in range(actions.shape[0]):
                    new_state = self._env._step(state, actions[[idx]])
                    new_value = self._alphabeta(new_state, depth - 1, piece_value, alpha, beta, True)
                    value = min(value, new_value)
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
        return value

    def state_value(self, State state, cnp.ndarray[double, ndim=1] piece_value):
        return (
            pop_count(state.black_rook) * piece_value[BLACK_ROOK]
            + pop_count(state.black_knight) * piece_value[BLACK_KNIGHT]
            + pop_count(state.black_bishop) * piece_value[BLACK_BISHOP]
            + pop_count(state.black_queen) * piece_value[BLACK_QUEEN]
            + pop_count(state.black_king) * piece_value[BLACK_KING]
            + pop_count(state.black_pawn) * piece_value[BLACK_PAWN]
            + pop_count(state.white_rook) * piece_value[WHITE_ROOK]
            + pop_count(state.white_knight) * piece_value[WHITE_KNIGHT]
            + pop_count(state.white_bishop) * piece_value[WHITE_BISHOP]
            + pop_count(state.white_queen) * piece_value[WHITE_QUEEN]
            + pop_count(state.white_king) * piece_value[WHITE_KING]
            + pop_count(state.white_pawn) * piece_value[WHITE_PAWN]
        )
