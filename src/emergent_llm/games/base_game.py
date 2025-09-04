"""Base game class for social dilemma experiments."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd
from emergent_llm.common import Action, GameDescription, GameHistory
from emergent_llm.players.base_player import BasePlayer
from numpy.typing import NDArray


@dataclass
class GameResult:
    """Results from a single game."""
    player_ids: list[str]  # Player names/IDs
    total_payoffs: list[float]  # Total scores by player
    total_cooperations: list[int]  # Number of cooperate actions by player
    cooperations_by_round: list[int]  # Number of cooperate actions in each round
    history: GameHistory  # Complete game history
    description: GameDescription  # Game parameters and rules

    def log_match_result(self, match_id: str = "", logger=None) -> str:
        """Log match result in clean DataFrame format."""
        lines = []

        # Header
        lines.append("=" * 60)
        if match_id:
            lines.append(f"MATCH: {match_id}")
        lines.append("=" * 60)

        # Player list with their actual names and strategies
        lines.append("PLAYERS:")
        for i, player_name in enumerate(self.player_ids):
            lines.append(f"  {i}: {player_name}")
        lines.append("")

        lines.append("ACTIONS:")
        actions_df = pd.DataFrame(self.history.actions_as_string_array())
        lines.append(actions_df.to_string(index=True))
        lines.append("")

        lines.append("PAYOFFS:")
        payoffs_df = pd.DataFrame(self.history.payoffs)
        lines.append(payoffs_df.to_string(index=True, float_format='%.3f'))
        lines.append("")

        # Final scores
        lines.append("TOTAL SCORES:")
        for i, total_payoff in enumerate(self.total_payoffs):
            lines.append(f"  Player {i}: {total_payoff:.3f}")
        lines.append(f"Average: {np.mean(self.total_payoffs):.3f}")
        lines.append("=" * 60)

        result_str = "\n".join(lines)

        if logger:
            logger.info(result_str)

        return result_str


class BaseGame(ABC):
    """Abstract base class for social dilemma games."""

    def __init__(self, players: Sequence[BasePlayer],
                 description: GameDescription):
        """Initialize game with players and description."""
        if len(players) != description.n_players:
            raise ValueError(
                f"Number of players ({len(players)}) must match "
                f"description.n_players ({description.n_players})"
            )

        self.players: list[BasePlayer] = players
        self.description: GameDescription = description

        # Initialize game state
        self.history: GameHistory | None = None
        self.current_round: int = 0

    @abstractmethod
    def _calculate_payoffs(self, actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round given actions."""

    def _play_round(self, players: list[BasePlayer]):
        """Play a single round of the game."""
        action_enums = [player(None) if self.history is None
                        else player(self.history.for_player(i))
                        for i, player in enumerate(players)]

        actions = Action.to_bool_array(action_enums)

        # Calculate payoffs for this round
        payoffs = self._calculate_payoffs(actions)

        if self.history is None:
            self.history = GameHistory(
                actions=actions,
                payoffs=payoffs
               )
        else:
            self.history.update(actions, payoffs)

        self.current_round += 1

    def play_game(self) -> GameResult:
        """Play a complete game for the number of rounds specified in description."""
        self.reset()

        for _ in range(self.description.n_rounds):
            self._play_round(self.players)

        assert self.history is not None

        return GameResult(
            player_ids=[p.name for p in self.players],
            total_payoffs=self.history.total_payoffs(),
            total_cooperations=self.history.total_cooperations(),
            cooperations_by_round=self.history.cooperations_by_round(),
            history=self.history,
            description=self.description
        )

    def reset(self):
        """Reset game to initial state."""
        self.history = None
        self.current_round = 0
        for player in self.players:
            player.reset()
