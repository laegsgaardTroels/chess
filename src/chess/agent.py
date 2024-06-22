from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt
from chess._constants import (
    BOARD,
    VERBOSE,
    MAX_ROUNDS,
    LOGO,
    EMPTY,
    BLACK_ROOK,
    BLACK_KNIGHT,
    BLACK_BISHOP,
    BLACK_QUEEN,
    BLACK_KING,
    BLACK_PAWN,
    WHITE_ROOK,
    WHITE_KNIGHT,
    WHITE_BISHOP,
    WHITE_QUEEN,
    WHITE_KING,
    WHITE_PAWN,
    WHITE,
    BLACK,
    STATE_DTYPE,
    ACTION_DTYPE,
)
from chess import _movegen
from chess import _utils
from chess._version import __version__


State = npt.NDArray
Action = npt.NDArray


class Agent(ABC):
    def __init__(self, color):
        self.color = color  # FIXME: Is this needed?

    @abstractmethod
    def policy(self, state: State) -> Action:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


def parse(agent: str) -> Agent:
    return eval(agent)


class RandomAgent(Agent):
    def __init__(self, seed: int = 42):
        self.seed = seed

    def policy(self, state):
        choices = _movegen.actions(state)
        action = np.empty(1, ACTION_DTYPE)
        action[:] = np.random.choice(choices)
        return action

    def __repr__(self):
        return "RandomAgent()"


class HumanAgent(Agent):
    """A human agent (TODO: Finish this)."""

    def policy(self, state: State) -> Action:
        actions_ = _movegen.actions(state)
        print(
            "\n".join(
                [f"{idx:<3}: {_utils.actionstr(a)}" for idx, a in enumerate(
                    actions_)]
            )
            + "\n"
        )
        action_idx = int(input("Select action : "))
        return actions_[action_idx]

    def __repr__(self):
        return "HumanAgent()"


class AlphaBetaAgent(Agent):
    """Agent using minimax with alpha-beta pruning."""

    def __init__(
        self,
        color: int,
        depth=2,
        piece_value: dict[str, float] = {
            "Empty": 0,
            "Pawn": 1,
            "Knight": 3,
            "Bishop": 3,
            "Rook": 5,
            "Queen": 9,
            "King": 1e6,
        },
    ):
        super().__init__(color=color)
        self.depth = depth
        self.piece_value = piece_value

    @property
    def _piece_value(self) -> dict[int, float]:
        piece_value = self.piece_value
        if self.color == WHITE:
            return {
                EMPTY: piece_value["Empty"],
                BLACK_ROOK: -piece_value["Rook"],
                BLACK_KNIGHT: -piece_value["Knight"],
                BLACK_BISHOP: -piece_value["Bishop"],
                BLACK_QUEEN: -piece_value["Queen"],
                BLACK_KING: -piece_value["King"],
                BLACK_PAWN: -piece_value["Pawn"],
                WHITE_ROOK: piece_value["Rook"],
                WHITE_KNIGHT: piece_value["Knight"],
                WHITE_BISHOP: piece_value["Bishop"],
                WHITE_QUEEN: piece_value["Queen"],
                WHITE_KING: piece_value["King"],
                WHITE_PAWN: piece_value["Pawn"],
            }
        elif self.color == BLACK:
            return {
                EMPTY: piece_value["Empty"],
                BLACK_ROOK: piece_value["Rook"],
                BLACK_KNIGHT: piece_value["Knight"],
                BLACK_BISHOP: piece_value["Bishop"],
                BLACK_QUEEN: piece_value["Queen"],
                BLACK_KING: piece_value["King"],
                BLACK_PAWN: piece_value["Pawn"],
                WHITE_ROOK: -piece_value["Rook"],
                WHITE_KNIGHT: -piece_value["Knight"],
                WHITE_BISHOP: -piece_value["Bishop"],
                WHITE_QUEEN: -piece_value["Queen"],
                WHITE_KING: -piece_value["King"],
                WHITE_PAWN: -piece_value["Pawn"],
            }
        else:
            raise NotImplementedError()

    def state_value(self, state):
        total_value = 0
        for piece, value in self._piece_value.items():
            total_value = total_value + np.sum(state["board"] == piece) * value
        return total_value

    def policy(self, state):
        best_actions = []
        max_value = -np.inf
        for action in _movegen.actions(state):
            new_state = _movegen.step(state, action)
            value = _movegen.alphabeta(
                state=new_state,
                depth=self.depth - 1,
                piece_value=self._piece_value,
                maximizing_player=False,
            )
            # value = self.alphabeta(
            #    state=new_state, depth=self.depth - 1, maximizing_player=False
            # )
            if value == max_value:
                best_actions.append(action)
            elif value > max_value:
                best_actions = [action]
                max_value = value

        return np.random.choice(best_actions)

    def alphabeta(
        self,
        state,
        depth,
        alpha=-np.inf,
        beta=np.inf,
        maximizing_player=True,
    ):
        """Minimax with alpha-beta pruning."""

        if depth == 0:
            value = self.state_value(state)
        else:
            if maximizing_player:
                value = -np.inf
                for action in _movegen.actions(state):
                    new_state = _movegen.step(state, action)
                    new_value = self.alphabeta(
                        new_state, depth - 1, alpha, beta, False)
                    value = max(value, new_value)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            else:
                value = np.inf
                for action in _movegen.actions(state):
                    new_state = _movegen.step(state, action)
                    new_value = self.alphabeta(
                        new_state, depth - 1, alpha, beta, True)
                    value = min(value, new_value)
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
        return value

    def __repr__(self) -> str:
        return (
            f"AlphaBetaAgent(color={self.color}, "
            f"depth={self.depth}, "
            f"piece_value={self.piece_value})"
        )


def simulate(
    white_player: Agent,
    black_player: Agent,
    color: int = WHITE,
    board: str = BOARD,
    verbose: bool = VERBOSE,
    max_rounds: int = MAX_ROUNDS,
):
    state = _utils.init_state(color=color, board=board)

    state_log = np.empty(shape=(max_rounds,), dtype=STATE_DTYPE)
    action_log = np.empty(shape=(max_rounds,), dtype=ACTION_DTYPE)

    idx = 1

    if verbose:
        print(LOGO)
        print("version", __version__)
        print(f"White player: {white_player}")
        print(f"Black player: {black_player}")
        print()
        print()
    try:
        for idx in range(max_rounds):
            if verbose:
                print(f"Round {idx + 1}")
                print(_utils.statestr(state))
                print()

            if state["color"]:
                action = white_player.policy(state)
            else:
                action = black_player.policy(state)

            state_log[idx] = state
            action_log[idx] = action

            state = _movegen.step(state, action)

            if verbose:
                if state["white_checkmate"]:
                    print(_utils.statestr(state))
                    print()
                    print("White won!")
                    break

                if state["black_checkmate"]:
                    print(_utils.statestr(state))
                    print()
                    print("Black won!")
                    break

                if state["draw"]:
                    print(_utils.statestr(state))
                    print()
                    print("Draw!")
                    break

    except KeyboardInterrupt:
        if verbose:
            print()
            print()
            print("Game stopped")

    state_log = state_log[: idx + 1]
    action_log = action_log[: idx + 1]

    return state_log, action_log


simulate.__doc__ = f"""Simulate a chess game between two agents.

Args:
    white_player (Agent): The agent playing a the white player.
    black_player (Agent): The agent playing a the black player.
    color (int): The color that is currently playing encoded as an integer
        where white={WHITE} and black={BLACK}. Default is white={WHITE}.
    board (str): The board set as a unicode string. Default is {BOARD}
    verbose (bool): Should the game be printed to stdout. Default is {VERBOSE}.
    max_rounds (int): Maximum number of rounds before the game is terminated.
        Default is {MAX_ROUNDS}.

Returns:
    tuple[NDArray, NDArray]: A with two numpy structured
        arrays containing the state and action log. The state log
        contains the states that was visited during the game and the
        action log contains the action that each agent selected.
"""
