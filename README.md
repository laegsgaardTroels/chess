# chess
[![CI Tests](https://github.com/laegsgaardTroels/chess/actions/workflows/ci.yml/badge.svg)](https://github.com/laegsgaardTroels/chess/actions/workflows/ci.yml)

An implementation of chess using numpy and cython.


## Installation

git clone the repository and run the default make target for intallation.

```bash
git clone git@github.com:laegsgaardTroels/chess.git
make
```

Make installs the `chess` package in a `venv/`. In below it is assumed the `venv/` is activated.

```bash
source venv/bin/activate
```

## Gameplay

The gameplay is through a cli installed by the chess package. See the help message for documentation:

```bash
chess -h
# usage: chess [-h] [-c COLOR] [-b BOARD] [-v] [-m MAX_ROUNDS] white_player black_player
# 
# Chess engine command line interface
# 
# positional arguments:
#   white_player          white_player (Agent): The agent playing a the white player
#   black_player          black_player (Agent): The agent playing a the black player
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -c COLOR, --color COLOR
#                         The color that is currently playing encoded as an integer where white=1 and black=0. Default is 1
#   -b BOARD, --board BOARD
#                         The board set as a unicode string. Default is ♜♞♝♛♚♝♞♜♟♟♟♟♟♟♟♟ ♙♙♙♙♙♙♙♙♖♘♗♕♔♗♘♖
#   -v, --verbose         Should the game be printed to stdout. Default is False
#   -m MAX_ROUNDS, --max-rounds MAX_ROUNDS
#                         Maximum number of rounds before the game is terminated. Default is 5000
```

Example human vs machine play:

```bash
chess -v "HumanAgent()" "AlphaBetaAgent(depth=3)"
```

Example machine vs machine play:

```bash
chess -v "AlphaBetaAgent(depth=3)" "AlphaBetaAgent(depth=3)"
```

## Contributing

Feel free to make a branch with a pull request.

## Missing Things

The game is a simplifid version of chess. It does not yet support en passant, the threefold repetition and other more complex rules of chess.
