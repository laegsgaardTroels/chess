from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt
from chess._constants import (
    BOARD,
    VERBOSE,
    MAX_ROUNDS,
    LOGO,
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
from chess._environment import Environment, AlphaBetaSearch
from chess import _utils
from chess._version import __version__


State = npt.NDArray
Action = npt.NDArray


class Agent(ABC):
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
        self._env = Environment()
        self.seed = seed
        np.random.seed(self.seed)

    def policy(self, state):
        choices = self._env.actions(state)
        action = np.empty(1, ACTION_DTYPE)
        action[:] = np.random.choice(choices)
        return action

    def __repr__(self):
        return f"RandomAgent({self.seed=})"


class HumanAgent(Agent):
    def __init__(self):
        self._env = Environment()

    def policy(self, state: State) -> Action:
        actions_ = self._env.actions(state)
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
        depth=2,
        piece_value: dict[str, float] = {
            "Pawn": 1,
            "Knight": 3,
            "Bishop": 3,
            "Rook": 5,
            "Queen": 9,
            "King": 1e6,
        },
    ):
        self.depth = depth
        self.piece_value = piece_value
        self._alpha_beta_search = AlphaBetaSearch()

    def _piece_value(self, white_player_turn: bool):
        piece_value = np.zeros(shape=12)
        piece_value[BLACK_ROOK] = -self.piece_value["Rook"]
        piece_value[BLACK_KNIGHT] = -self.piece_value["Knight"]
        piece_value[BLACK_BISHOP] = -self.piece_value["Bishop"]
        piece_value[BLACK_QUEEN] = -self.piece_value["Queen"]
        piece_value[BLACK_KING] = -self.piece_value["King"]
        piece_value[BLACK_PAWN] = -self.piece_value["Pawn"]
        piece_value[WHITE_ROOK] = self.piece_value["Rook"]
        piece_value[WHITE_KNIGHT] = self.piece_value["Knight"]
        piece_value[WHITE_BISHOP] = self.piece_value["Bishop"]
        piece_value[WHITE_QUEEN] = self.piece_value["Queen"]
        piece_value[WHITE_KING] = self.piece_value["King"]
        piece_value[WHITE_PAWN] = self.piece_value["Pawn"]
        if white_player_turn:
            return piece_value
        else:
            return -piece_value

    def policy(self, state):
        piece_value = self._piece_value(bool(state["white_player_turn"]))
        actions, values = self._alpha_beta_search.search(
            state, self.depth, piece_value)
        optimal_actions = actions[values == np.max(values)]
        return np.random.choice(optimal_actions)

    def __repr__(self) -> str:
        return f"AlphaBetaAgent(depth={self.depth}, piece_value={self.piece_value})"


def simulate(
    white_player: Agent,
    black_player: Agent,
    color: int = WHITE,
    board: str = BOARD,
    verbose: bool = VERBOSE,
    max_rounds: int = MAX_ROUNDS,
):
    _env = Environment()
    state = _utils.state_init(color=color, board=board)

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
                print(_utils.state_str(state))
                print()

            if state["white_player_turn"]:
                action = white_player.policy(state)
            else:
                action = black_player.policy(state)

            state_log[idx] = state
            action_log[idx] = action

            state = _env.step(state, action)

            if verbose:
                if state["is_white_checkmate"]:
                    print(_utils.state_str(state))
                    print()
                    print("Black won!")
                    break

                if state["is_black_checkmate"]:
                    print(_utils.state_str(state))
                    print()
                    print("White won!")
                    break

                if state["is_draw"]:
                    print(_utils.state_str(state))
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
