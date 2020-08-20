"""The main program used to run the chess game.
"""
from chess.agent import HumanAgent
from chess.agent import AlphaBetaAgent
from chess.agent import RandomAgent
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
        white_player=AlphaBetaAgent,
        black_player=RandomAgent,
    )
else:
    game = Game(
        white_player=HumanAgent,
        black_player=AlphaBetaAgent,
    )

game.play(verbose=True)
