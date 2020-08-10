"""The main program used to run the chess game.
"""
from chess.agent import AlphaBetaAgent
from chess.game import Game

import logging


logging.basicConfig(
    filename='game.log',
    filemode='w',
    level=logging.INFO
)
agent = AlphaBetaAgent()
game = Game()
game.play(agent)
