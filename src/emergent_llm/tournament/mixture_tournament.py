"""Mixture tournament for a single group size."""
import random
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import numpy as np
import pandas as pd
from emergent_llm.common import Attitude, GameDescription
from emergent_llm.players import BasePlayer
from emergent_llm.tournament.base_tournament import BaseTournament, BaseTournamentConfig
from emergent_llm.tournament.results import MatchResult, MixtureResult, MixtureTournamentResults


class MixtureTournament(BaseTournament):
    """Tournament testing different mixtures of cooperative vs aggressive players for a single group size."""

    def __init__(self, cooperative_players: list[BasePlayer], aggressive_players: list[BasePlayer], config: BaseTournamentConfig):
        """
        Initialize mixture tournament.

        Args:
            cooperative_players: List of cooperative players
            aggressive_players: List of aggressive players
            config: Tournament configuration
        """
        super().__init__(config)
        self.cooperative_players: list[BasePlayer] = cooperative_players
        self.aggressive_players: list[BasePlayer] = aggressive_players


        group_size = config.game_description.n_players

        # Validate we have enough strategies
        if len(cooperative_players) < group_size:
            raise ValueError(f"Need at least {group_size} cooperative players, got {len(cooperative_players)}")
        if len(aggressive_players) < group_size:
            raise ValueError(f"Need at least {group_size} aggressive players, got {len(aggressive_players)}")

        self.mixture_stats: dict[tuple, MixtureResult] = {}

    def run_tournament(self) -> MixtureTournamentResults:
        """Run tournament across all mixture ratios for this group size."""
        group_size = self.config.game_description.n_players
        self.logger.info(f"Running mixture tournament for group size {group_size}")

        # Test all possible mixtures
        for n_aggressive in range(group_size + 1):
            n_cooperative = group_size - n_aggressive
            mixture_key = (n_cooperative, n_aggressive)

            # Initialize stats for this mixture
            self.mixture_stats[mixture_key] = MixtureResult(
                group_size=group_size,
                n_cooperative=n_cooperative,
                n_aggressive=n_aggressive,
                cooperative_scores=[],
                aggressive_scores=[],
                matches_played=0
            )

            self._run_mixture(mixture_key)

        return MixtureTournamentResults(
            match_results=self.match_results,
            mixture_results=list(self.mixture_stats.values()),
            game_description=self.config.game_description,
            repetitions=self.config.repetitions
        )

    def _run_mixture(self, mixture_key: tuple[int, int]):
        """Run multiple matches for a specific mixture"""

        self.logger.info(f"Testing mixture: {mixture_key}")

        for match_num in range(self.config.repetitions):
            # Create players for this match
            match_players = self._create_match_players(mixture_key)
            match_id = f"mixture_{mixture_key}a_match{match_num:04d}"

            # Run the match using base class method
            match_result = self._run_match(match_players, match_id)

            # Record mixture-specific stats
            self._record_match_stats(mixture_key, match_players, match_result)

    def _create_match_players(self, mixture_key: tuple[int, int]) -> list[BasePlayer]:
        """Create players for a single match by sampling from available strategies."""
        players = []

        # Sample cooperative players
        if mixture_key[0] > 0:
            players.extend(random.sample(self.cooperative_players, mixture_key[0]))

        # Sample aggressive players
        if mixture_key[1] > 0:
            players.extend(random.sample(self.aggressive_players, mixture_key[1]))

        # Shuffle to randomize positions
        random.shuffle(players)
        return players

    def _record_match_stats(self, mixture_key: tuple, players: list[BasePlayer], match_result: MatchResult):
        """Record statistics for a completed match."""
        stats = self.mixture_stats[mixture_key]

        # Record payoffs by player type
        for player, payoff in zip(players, match_result.payoffs):
            if hasattr(player, 'attitude'):
                if player.attitude == Attitude.COOPERATIVE:
                    stats.cooperative_scores.append(payoff)
                elif player.attitude == Attitude.AGGRESSIVE:
                    stats.aggressive_scores.append(payoff)
                else:
                    self.logger.warning(f"Player {player.name} has unknown attitude: {player.attitude}")
            else:
                self.logger.warning(f"Player {player.name} has no attitude attribute")
