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
BLACK_ROOK = 1
BLACK_KNIGHT = 2
BLACK_BISHOP = 3
BLACK_QUEEN = 4
BLACK_KING = 5
BLACK_PAWN = 6
WHITE_ROOK = 7
WHITE_KNIGHT = 8
WHITE_BISHOP = 9
WHITE_QUEEN = 10
WHITE_KING = 11
WHITE_PAWN = 12
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
PIECE_STRS = {
    BLACK_ROOK: "♜",
    BLACK_KNIGHT: "♞",
    BLACK_BISHOP: "♝",
    BLACK_QUEEN: "♛",
    BLACK_KING: "♚",
    BLACK_PAWN: "♟",
    WHITE_ROOK: "♖",
    WHITE_KNIGHT: "♘",
    WHITE_BISHOP: "♗",
    WHITE_QUEEN: "♕",
    WHITE_KING: "♔",
    WHITE_PAWN: "♙",
}
NO_CASTLING = (False, False, False, False)
NO_PROMOTION = (False, False, False, False, False)
CASTLING_DTYPE = [
    ("left_black", "?"),
    ("right_black", "?"),
    ("left_white", "?"),
    ("right_white", "?"),
]
STATE_DTYPE = [
    ("color", "?"),
    ("board", "<i8", (8, 8)),
    (
        "castling",
        CASTLING_DTYPE,
    ),
    ("white_checkmate", "?"),
    ("black_checkmate", "?"),
    ("draw", "?"),
]
POSITION_DTYPE = [("i", "<i8"), ("j", "<i8")]
ACTION_DTYPE = [
    ("piece", "<i8"),
    ("src", POSITION_DTYPE),
    ("dst", POSITION_DTYPE),
    (
        "castling",
        CASTLING_DTYPE,
    ),
    (
        "promotion",
        [
            ("rook", "?"),
            ("knight", "?"),
            ("bishop", "?"),
            ("queen", "?"),
            ("pawn", "?"),
        ],
    ),
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
