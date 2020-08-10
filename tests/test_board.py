from chess.game import Game


def test_checkmate():
    """Can't initialize a new game with checkmate."""

    game = Game()

    assert not game.is_check('white'), (
        "Not checkmate in first round."
    )
    assert not game.is_check('black'), (
        "Not checkmate in first round."
    )
    assert not game.is_checkmate('white'), (
        "Not checkmate in first round."
    )
    assert not game.is_checkmate('black'), (
        "Not checkmate in first round."
    )
