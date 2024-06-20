from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt
from chess._constants import (
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
    ACTION_DTYPE,
)
from chess import _movegen
from chess import _utils


State = npt.NDArray
Action = npt.NDArray


class Agent(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def policy(self, state: State) -> Action:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


class RandomAgent(Agent):
    def policy(self, state):
        choices =_movegen.actions(state)
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
                [f"{idx:<3}: {_utils.actionstr(a)}" for idx, a in enumerate(actions_)]
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
            value = self.alphabeta(
                state=new_state, depth=self.depth - 1, maximizing_player=False
            )
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
                    new_value = self.alphabeta(new_state, depth - 1, alpha, beta, False)
                    value = max(value, new_value)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            else:
                value = np.inf
                for action in _movegen.actions(state):
                    new_state = _movegen.step(state, action)
                    new_value = self.alphabeta(new_state, depth - 1, alpha, beta, True)
                    value = min(value, new_value)
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
        return value

    def __repr__(self) -> str:
        return f"AlphaBetaAgent(color={self.color}, depth={self.depth}, piece_value={self.piece_value})"
