"""Mixture tournament for a single group size."""
import random
from dataclasses import asdict, dataclass, fields

from emergent_llm.players import LLMPlayer
from emergent_llm.tournament.base_tournament import BaseTournament
from emergent_llm.tournament.configs import BaseTournamentConfig, MixtureKey
from emergent_llm.tournament.results import MixtureTournamentResults


class MixtureTournament(BaseTournament):
    """Tournament testing different mixtures of collective vs exploitative players for a single group size."""

    def __init__(self, collective_players: list[LLMPlayer],
                 exploitative_players: list[LLMPlayer],
                 config: BaseTournamentConfig):
        """
        Initialize mixture tournament.

        Args:
            collective_players: List of collective players
            exploitative_players: List of exploitative players
            config: Tournament configuration
        """
        super().__init__(config)
        self.collective_players: list[LLMPlayer] = collective_players
        self.exploitative_players: list[LLMPlayer] = exploitative_players

        group_size = config.game_description.n_players

        # Validate we have enough strategies
        if len(collective_players) < group_size:
            raise ValueError(
                f"Need at least {group_size} collective players, got {len(collective_players)}"
            )
        if len(exploitative_players) < group_size:
            raise ValueError(
                f"Need at least {group_size} exploitative players, got {len(exploitative_players)}"
            )

    def run_tournament(self) -> MixtureTournamentResults:
        """Run tournament across all mixture ratios for this group size."""
        group_size = self.config.game_description.n_players
        self.logger.info(
            f"Running mixture tournament for group size {group_size}")

        # Step size: for large tournaments, only test every 4th
        # This is a bit hacky
        step_size = max(1, group_size // 64)
        # Test all possible mixtures
        for n_exploitative in range(0, group_size + 1, step_size):
            n_collective = group_size - n_exploitative
            mixture_key = MixtureKey(n_collective, n_exploitative)

            self._run_mixture(mixture_key)

        return MixtureTournamentResults(
            config=self.config,
            collective_player_ids=[p.id for p in self.collective_players],
            exploitative_player_ids=[p.id for p in self.exploitative_players],
            match_results=self.match_results)

    def _run_mixture(self, mixture_key: MixtureKey):
        """Run multiple matches for a specific mixture"""

        self.logger.info(f"Testing mixture: {mixture_key}")

        for match_num in range(self.config.repetitions):
            # Create players for this match
            match_players = self._create_match_players(mixture_key)
            match_id = f"mixture_{mixture_key}_match{match_num:04d}"

            # Run the match using base class method
            match_result = self._run_match(match_players, match_id)

    def _create_match_players(self, mixture_key: MixtureKey) -> list[LLMPlayer]:
        """Create players for a single match by sampling from available strategies."""
        players = []

        # Sample collective players
        if mixture_key.n_collective > 0:
            players.extend(
                random.sample(self.collective_players,
                              mixture_key.n_collective))

        # Sample exploitative players
        if mixture_key.n_exploitative > 0:
            players.extend(
                random.sample(self.exploitative_players,
                              mixture_key.n_exploitative))

        # Shuffle to randomize positions
        random.shuffle(players)
        return players
