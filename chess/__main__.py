"""The main program used to run the chess game.
"""
from chess.agent import HumanAgent
from chess.agent import AlphaBetaAgent
from chess.game import Game

import cProfile
import argparse

import logging


def self_play(verbose=True):
    game = Game(
        white_player=AlphaBetaAgent,
        black_player=AlphaBetaAgent,
    )
    game.play(verbose=verbose)


def human_vs_machine():
    game = Game(
        white_player=HumanAgent,
        black_player=AlphaBetaAgent,
    )
    game.play(verbose=True)


def profiling():
    cProfile.run('self_play(verbose=False)', sort='time')


parser = argparse.ArgumentParser(
    description='Control the gameplay.',
)
parser.add_argument(
    'cmd',
    metavar='cmd',
    type=str,
    choices=['self_play', 'human_vs_machine', 'human_vs_human', 'profiling'],
    help="Should the game be self play or against a human player."
)
args = parser.parse_args()


logging.basicConfig(
    filename='game.log',
    filemode='w',
    level=logging.INFO
)

if args.cmd == 'self_play':
    self_play()

elif args.cmd == 'human_vs_machine':
    human_vs_machine()

elif args.cmd == 'profiling':
    profiling()

else:
    raise ValueError(f"Unknown command {args.cmd}")
