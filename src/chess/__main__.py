import argparse
from chess import _agent
from chess._constants import BOARD, WHITE, BLACK, MAX_ROUNDS, VERBOSE, COLOR


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chess engine command line interface",
    )
    parser.add_argument(
        "white_player",
        help="white_player (Agent): The agent playing a the white player",
        type=str,
    )
    parser.add_argument(
        "black_player",
        help="black_player (Agent): The agent playing a the black player",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--color",
        help=(
            "The color that is currently playing encoded as an integer "
            f"where white={WHITE} and black={BLACK}. Default is {COLOR}"
        ),
        default=COLOR,
        required=False,
        type=int,
    )
    parser.add_argument(
        "-b",
        "--board",
        help=(f"The board set as a unicode string. Default is {BOARD}"),
        default=BOARD,
        required=False,
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help=f"Should the game be printed to stdout. Default is {VERBOSE}",
        default=VERBOSE,
        required=False,
    )
    parser.add_argument(
        "-m",
        "--max-rounds",
        help=(
            "Maximum number of rounds before the game is terminated. "
            f"Default is {MAX_ROUNDS}"
        ),
        default=MAX_ROUNDS,
        required=False,
        type=int,
    )

    args = parser.parse_args()

    _agent.simulate(
        white_player=_agent.parse(args.white_player),
        black_player=_agent.parse(args.black_player),
        color=args.color,
        board=args.board,
        verbose=args.verbose,
        max_rounds=args.max_rounds,
    )


if __name__ == "__main__":
    main()
