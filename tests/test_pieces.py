from chess.board import Board

from chess.pieces import Tower
from chess.pieces import Horse
from chess.pieces import Bishop
from chess.pieces import King
from chess.pieces import Queen
from chess.pieces import Pawn
from chess.pieces import Empty


import pytest

from itertools import product

pieces = [
    King('white'),
    Queen('white'),
    Horse('white'),
    Bishop('white'),
    Tower('white'),
    Pawn('white'),
]


@pytest.mark.parametrize("piece", pieces)
def test_no_moves_outside_board(piece):
    """Test that a piece cannot move outside the board."""
    for i in range(8):
        for j in range(8):
            new_board = Board(
                [
                    [
                        Empty() for i in range(8)
                    ] for j in range(8)
                ]
            )
            new_board[i, j] = piece
            for move in piece.moves():
                assert move in product(range(8), range(8)), (
                    f"Move {move} for piece {type(piece)} "
                    "is outside of the board.\n\n"
                    f"{new_board}"
                )


@pytest.mark.parametrize("piece", pieces)
def test_no_move_to_current_position(piece):
    """Test that a piece cannot move to its current position."""
    for i in range(8):
        for j in range(8):
            new_board = Board(
                [
                    [
                        Empty() for i in range(8)
                    ] for j in range(8)
                ]
            )
            new_board[i, j] = piece

            for move in piece.moves():
                assert move != (i, j), (
                    f"Move {move} for piece {type(piece)} "
                    "is current position.\n\n"
                    f"{new_board}"
                )
