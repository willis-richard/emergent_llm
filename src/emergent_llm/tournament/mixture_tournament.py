"""Mixture tournament for a single group size."""
import random

from emergent_llm.players import LLMPlayer
from emergent_llm.tournament.base_tournament import BaseTournament
from emergent_llm.tournament.configs import BaseTournamentConfig
from emergent_llm.tournament.results import MixtureTournamentResults


from dataclasses import dataclass, asdict, fields


@dataclass
class MixtureKey:
    n_cooperative: int
    n_aggressive: int


class MixtureTournament(BaseTournament):
    """Tournament testing different mixtures of cooperative vs aggressive players for a single group size."""

    def __init__(self, cooperative_players: list[LLMPlayer], aggressive_players: list[LLMPlayer], config: BaseTournamentConfig):
        """
        Initialize mixture tournament.

        Args:
            cooperative_players: List of cooperative players
            aggressive_players: List of aggressive players
            config: Tournament configuration
        """
        super().__init__(config)
        self.cooperative_players: list[LLMPlayer] = cooperative_players
        self.aggressive_players: list[LLMPlayer] = aggressive_players


        group_size = config.game_description.n_players

        # Validate we have enough strategies
        if len(cooperative_players) < group_size:
            raise ValueError(f"Need at least {group_size} cooperative players, got {len(cooperative_players)}")
        if len(aggressive_players) < group_size:
            raise ValueError(f"Need at least {group_size} aggressive players, got {len(aggressive_players)}")

    def run_tournament(self) -> MixtureTournamentResults:
        """Run tournament across all mixture ratios for this group size."""
        group_size = self.config.game_description.n_players
        self.logger.info(f"Running mixture tournament for group size {group_size}")

        # Test all possible mixtures
        for n_aggressive in range(group_size + 1):
            n_cooperative = group_size - n_aggressive
            mixture_key = MixtureKey(n_cooperative, n_aggressive)

            self._run_mixture(mixture_key)

        return MixtureTournamentResults(
            config=self.config,
            cooperative_player_ids=[p.id for p in self.cooperative_players],
            aggressive_player_ids=[p.id for p in self.aggressive_players],
            match_results=self.match_results
        )

    def _run_mixture(self, mixture_key: MixtureKey):
        """Run multiple matches for a specific mixture"""

        self.logger.info(f"Testing mixture: {mixture_key}")

        for match_num in range(self.config.repetitions):
            # Create players for this match
            match_players = self._create_match_players(mixture_key)
            match_id = f"mixture_{mixture_key}a_match{match_num:04d}"

            # Run the match using base class method
            match_result = self._run_match(match_players, match_id)

    def _create_match_players(self, mixture_key: MixtureKey) -> list[LLMPlayer]:
        """Create players for a single match by sampling from available strategies."""
        players = []

        # Sample cooperative players
        if mixture_key.n_cooperative > 0:
            players.extend(random.sample(self.cooperative_players, mixture_key.n_cooperative))

        # Sample aggressive players
        if mixture_key.n_aggressive > 0:
            players.extend(random.sample(self.aggressive_players, mixture_key.n_aggressive))

        # Shuffle to randomize positions
        random.shuffle(players)
        return players
