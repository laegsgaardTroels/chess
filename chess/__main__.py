"""The main program used to run the chess game.
"""
from chess.agent import HumanAgent
from chess.agent import AlphaBetaAgent
from chess.game import Game

import argparse

import logging

parser = argparse.ArgumentParser(
    description='Control the gameplay.',
)
parser.add_argument(
    '--self_play',
    metavar='self_play',
    type=bool,
    help="Should the game be self play or against a human player."
)
args = parser.parse_args()


logging.basicConfig(
    filename='game.log',
    filemode='w',
    level=logging.INFO
)

if args.self_play:
    game = Game(
        black_player=AlphaBetaAgent,
        white_player=AlphaBetaAgent,
    )
else:
    game = Game(
        black_player=AlphaBetaAgent,
        white_player=HumanAgent,
    )

game.play()
