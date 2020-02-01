# -*- coding: utf-8 -*-
"""Test common checkmates.

References: https://en.wikipedia.org/wiki/Checkmate_pattern
"""

from chess import Game
from chess.pieces import *


def test_anastasia_s_mate():
    """"""
    game = Game([
        [Empty() for _ in range(8)],
        [Empty() for _ in range(4)] +
        [Horse('white'), Empty(), Pawn('black'), King('black')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(7)] + [Tower('white')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [King('white')] + [Empty() for _ in range(7)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_anderssen_s_mate():
    """"""
    game = Game([
        [Empty() for _ in range(6)] + [King('black'), Tower('white')],
        [Empty() for _ in range(6)] + [Pawn('white'), Empty()],
        [Empty() for _ in range(5)] + [King('white'), Empty(), Empty()],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_arabian_mate():
    """"""
    game = Game([
        [Empty() for _ in range(7)] + [King('black')],
        [Empty() for _ in range(7)] + [Tower('white')],
        [Empty() for _ in range(5)] + [Horse('white'), Empty(), Empty()],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_back_rank_mate():
    """"""
    game = Game([
        [Empty() for _ in range(3)] +
        [Tower('white'), Empty(), Empty(), King('black'), Empty()],
        [Empty() for _ in range(5)] +
        [Pawn('black'), Pawn('black'), Pawn('black')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_bishop_and_knight_mate():
    """"""
    game = Game([
        [Empty() for _ in range(7)] + [King('black')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(5)] +
        [Bishop('white'), King('white'), Horse('white')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_blackburne_s_mate():
    """"""
    game = Game([
        [Empty() for _ in range(5)] +
        [Tower('black'), King('black'), Empty()],
        [Empty() for _ in range(7)] + [Bishop('white')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(6)] +
        [Horse('white'), Empty()],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty(), Bishop('white')] + [Empty() for _ in range(6)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_black_swine_mate():
    """"""
    game = Game([
        [Empty() for _ in range(5)] +
        [Tower('black'), King('black'), Empty()],
        [Empty() for _ in range(6)] +
        [Tower('white'), Tower('white')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_bodens_mate():
    """"""
    game = Game([
        [Empty(),  Empty()] +
        [King('black'), Tower('black')] +
        [Empty() for _ in range(4)],
        [Empty() for _ in range(3)] +
        [Pawn('black')] +
        [Empty() for _ in range(4)],
        [Bishop('white')] + [Empty() for _ in range(7)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(5)] +
        [Bishop('white'), Empty(), Empty()],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_box_mate():
    """"""
    game = Game([
        [Tower('white'),  Empty(),  Empty()] +
        [King('black')] +
        [Empty() for _ in range(4)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(3)] +
        [King('white')] +
        [Empty() for _ in range(4)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_corner_mate():
    """"""
    game = Game([
        [Empty() for _ in range(7)] +
        [King('black')],
        [Empty() for _ in range(5)] +
        [Horse('white'), Empty(), Pawn('black')],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(6)] +
        [Tower('white'), Empty()],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_cozio_s_mate():
    """"""
    game = Game([
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(6)] +
        [Pawn('black'), Empty()],
        [Empty() for _ in range(5)] +
        [Queen('black'), King('black'), Empty()],
        [Empty() for _ in range(7)] + [Queen('white')],
        [Empty() for _ in range(6)] +
        [King('white'), Empty()],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_damiano_s_bishop_mate():
    """"""
    game = Game([
        [Empty() for _ in range(5)] +
        [King('black'), Empty(), Empty()],
        [Empty() for _ in range(5)] +
        [Queen('white'), Empty(), Empty()],
        [Empty() for _ in range(6)] +
        [Bishop('white'), Empty()],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(7)] +
        [King('white')],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)


def test_damiano_mate():
    """"""
    game = Game([
        [Empty() for _ in range(5)] +
        [Tower('black'), King('black'), Empty()],
        [Empty() for _ in range(6)] +
        [Pawn('black'), Queen('white')],
        [Empty() for _ in range(6)] +
        [Pawn('white'), Empty()],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(8)],
        [Empty() for _ in range(7)] +
        [King('white')],
    ])
    assert game.is_check('black'), print(game)
    assert game.is_checkmate('black'), print(game)
