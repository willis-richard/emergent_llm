"""Base game class for social dilemma experiments."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from emergent_llm.common import Action, GameDescription, GameHistory
from emergent_llm.players.base_player import BasePlayer


@dataclass
class GameResult:
    """Results from a single game."""
    players: list[str]  # Player names/IDs
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
        for i, player_name in enumerate(self.players):
            lines.append(f"  {i}: {player_name}")
        lines.append("")

        # Actions DataFrame - already correctly implemented
        lines.append("ACTIONS:")
        actions_df = self._create_actions_dataframe()
        lines.append(actions_df.to_string(index=True))  # Show round index
        lines.append("")

        # Payoffs DataFrame - already correctly implemented
        lines.append("PAYOFFS:")
        payoffs_df = self._create_payoffs_dataframe()
        lines.append(payoffs_df.to_string(index=True, float_format='%.3f'))  # Show round index
        lines.append("")

        # Final scores
        total_payoffs = self.history.payoffs.sum(axis=0)
        lines.append("TOTAL SCORES:")
        for i, total_payoff in enumerate(total_payoffs):
            lines.append(f"  Player {i}: {total_payoff:.3f}")
        lines.append(f"Average: {total_payoffs.mean():.3f}")
        lines.append("=" * 60)

        result_str = "\n".join(lines)

        if logger:
            logger.info(result_str)

        return result_str

    def _create_actions_dataframe(self) -> pd.DataFrame:
        """Create DataFrame with round and player actions."""
        data = {'round': range(1, len(self.history.actions) + 1)}

        # Add column for each player (convert bool to C/D)
        for player_idx in range(len(self.players)):
            player_actions = [str(Action(a)) for a in self.history.actions[:, player_idx]]
            data[str(player_idx)] = player_actions

        return pd.DataFrame(data)

    def _create_payoffs_dataframe(self) -> pd.DataFrame:
        """Create DataFrame with round and player payoffs."""
        data = {'round': range(1, len(self.history.payoffs) + 1)}

        # Add column for each player
        for player_idx in range(len(self.players)):
            data[str(player_idx)] = self.history.payoffs[:, player_idx]

        return pd.DataFrame(data)


class BaseGame(ABC):
    """Abstract base class for social dilemma games."""

    def __init__(self, players: list[BasePlayer],
                 description: GameDescription):
        """Initialize game with players and description."""
        if len(players) != description.n_players:
            raise ValueError(
                f"Number of players ({len(players)}) must match "
                f"description.n_players ({description.n_players})"
            )

        self.players: list[BasePlayer] = players
        self.description: GameDescription = description
        self.n_players: int = len(players)

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

        # Convert to boolean array explicitly
        actions = Action.to_bool_array(action_enums)

        # Validate the array type
        assert actions.dtype == np.bool_, f"Expected bool array, got {actions.dtype}"

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
        for player in self.players:
            player.reset()

        for _ in range(self.description.n_rounds):
            self._play_round(self.players)

        assert self.history is not None

        return GameResult(
            players=[self._get_player_display_name(player) for player in self.players],
            history=self.history,
            description=self.description
        )

    def _get_player_display_name(self, player: BasePlayer) -> str:
        """Get display name for player including strategy if available."""
        base_name = player.name
        if hasattr(player, 'strategy_name'):
            return f"{base_name}({player.strategy_name})"
        return base_name

    def reset(self):
        """Reset game to initial state."""
        self.history = None
        self.current_round = 0
