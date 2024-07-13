BOARD = (
    "♜♞♝♛♚♝♞♜"
    "♟♟♟♟♟♟♟♟"
    "        "
    "        "
    "        "
    "        "
    "♙♙♙♙♙♙♙♙"
    "♖♘♗♕♔♗♘♖"
)
EMPTY = 0
BLACK_ROOK = 0
BLACK_KNIGHT = 1
BLACK_BISHOP = 2
BLACK_QUEEN = 3
BLACK_KING = 4
BLACK_PAWN = 5
WHITE_ROOK = 6
WHITE_KNIGHT = 7
WHITE_BISHOP = 8
WHITE_QUEEN = 9
WHITE_KING = 10
WHITE_PAWN = 11
PIECES = [
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
PIECE_NAMES = [
    "black_rook",
    "black_knight",
    "black_bishop",
    "black_queen",
    "black_king",
    "black_pawn",
    "white_rook",
    "white_knight",
    "white_bishop",
    "white_queen",
    "white_king",
    "white_pawn",
]
PIECE_STRS = [
    "♜",
    "♞",
    "♝",
    "♛",
    "♚",
    "♟",
    "♖",
    "♘",
    "♗",
    "♕",
    "♔",
    "♙",
]
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
MAX_ROUNDS = 5000
LOGO = r"""
(  ____ \|\     /|(  ____ \(  ____ \(  ____ \
| (    \/| )   ( || (    \/| (    \/| (    \/
| |      | (___) || (__    | (_____ | (
| |      |  ___  ||  __)   (_____  )(_____  )
| |      | (   ) || (            ) |      ) |
| (____/\| )   ( || (____/\/\____) |/\____) |
(_______/|/     \|(_______/\_______)\_______)

"""
NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8]
REVERSED_NUMBERS = NUMBERS[::-1]  # i
LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h"]  # j
BLACK = 0
WHITE = 1
SEED = 42
VERBOSE = False
COLOR = WHITE
MAX_PLY = 5000
