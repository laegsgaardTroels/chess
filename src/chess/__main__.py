import argparse
import numpy as np
from chess import agent
from chess._utils import init_state, statestr
from chess import _movegen
from chess._constants import (
    STARTING_BOARD,
    WHITE,
    BLACK,
    MAX_ROUNDS,
    STATE_DTYPE,
    ACTION_DTYPE,
    LOGO,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chess engine command line interface.",
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Should the game be printed.",
        action='store_true',
        default=True,
    )
    subparsers = parser.add_subparsers(required=True)

    parser_machine_vs_machine = subparsers.add_parser(
        'machine_vs_machine',
        help="Let the machine play against itself."
    )
    parser_machine_vs_machine.set_defaults(func=machine_vs_machine)

    parser_human_vs_machine = subparsers.add_parser(
        'human_vs_machine',
        help="Play against the machine."
    )
    parser_human_vs_machine.set_defaults(func=human_vs_machine)

    args = parser.parse_args()
    args.func(args)


def machine_vs_machine(args: argparse.Namespace) -> None:
    simulate(
        white_player=agent.AlphaBetaAgent(color=WHITE),
        black_player=agent.AlphaBetaAgent(color=BLACK),
        verbose=args.verbose,
    )


def human_vs_machine(args: argparse.Namespace) -> None:
    simulate(
        white_player=agent.HumanAgent(color=WHITE),
        black_player=agent.AlphaBetaAgent(color=BLACK),
        verbose=args.verbose,
    )


def simulate(
    white_player: agent.Agent,
    black_player: agent.Agent,
    color=WHITE,
    board: str = STARTING_BOARD,
    verbose: bool = False,
    seed: int = 42,
    max_rounds: int = MAX_ROUNDS,
):
    """The main game loop."""

    np.random.seed(seed=seed)

    state = init_state(color=color, board=board)

    state_log = np.empty(shape=(max_rounds,), dtype=STATE_DTYPE)
    action_log = np.empty(shape=(max_rounds,), dtype=ACTION_DTYPE)

    idx = 1

    if verbose:
        print(LOGO)
        print(f"White player: {white_player}")
        print(f"Black player: {black_player}")
        print()
        print()
    try:
        for idx in range(max_rounds):
            if verbose:
                print(f"Round {idx}")
                print(statestr(state))
                print()

            if state["color"]:
                action = white_player.policy(state)
            else:
                action = black_player.policy(state)

            state_log[idx] = state
            action_log[idx] = action

            state = _movegen.step(state, action)

            if len(_movegen.actions(state)) != 0:
                continue
            else:
                if verbose:
                    print(statestr(state))
                    print()
                    if state["color"]:
                        print("White won!")
                    else:
                        print("Black won!")
                break

    except KeyboardInterrupt:
        if verbose:
            print()
            print()
            print("Game stopped")

    state_log = state_log[: idx + 1]
    action_log = action_log[: idx + 1]

    return state_log, action_log
