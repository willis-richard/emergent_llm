"""Mixture tournament testing different ratios of cooperative vs aggressive players."""
import logging
import random
from typing import List
import pandas as pd
import numpy as np
from pathlib import Path

from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.games.base_game import BaseGame
from emergent_llm.common import GameDescription
from emergent_llm.players import LLMPlayer, BasePlayer
from emergent_llm.common.attitudes import Attitude


class MixtureTournament(FairTournament):
    """Tournament testing different mixtures of cooperative vs aggressive players."""

    def __init__(self,
                 cooperative_players: List[BasePlayer],
                 aggressive_players: List[BasePlayer],
                 game_class: type[BaseGame],
                 game_description: GameDescription,
                 matches_per_mixture: int = 100,
                 verbose_logging: bool = False,
                 log_file: str = None):

        super().__init__([], game_class, game_description)

        self.cooperative_players = cooperative_players
        self.aggressive_players = aggressive_players
        self.matches_per_mixture = matches_per_mixture
        self.verbose_logging = verbose_logging

        # Validate that players have attitude attributes
        for player in cooperative_players:
            if not hasattr(player, 'attitude') or player.attitude != Attitude.COOPERATIVE:
                self.logger.warning(f"Player {player.name} doesn't have COOPERATIVE attitude")

        for player in aggressive_players:
            if not hasattr(player, 'attitude') or player.attitude != Attitude.AGGRESSIVE:
                self.logger.warning(f"Player {player.name} doesn't have AGGRESSIVE attitude")

    def _create_match_players(self, n_cooperative: int, n_aggressive: int, match_num: int) -> List[BasePlayer]:
        """Create players for a single match."""
        players = []

        # Sample cooperative players
        if n_cooperative > 0:
            players.extend(random.sample(self.cooperative_players, n_cooperative))

        # Sample aggressive players
        if n_aggressive > 0:
            players.extend(random.sample(self.aggressive_players, n_aggressive))

        # Shuffle to randomize positions
        random.shuffle(players)
        return players

    def _calculate_mixture_averages(self, mixture_results, n_cooperative: int):
        """Calculate average scores by player type using attitude attribute."""
        cooperative_scores = []
        aggressive_scores = []

        for result in mixture_results:
            total_payoffs = result.history.payoffs.sum(axis=0)

            # Get the actual players used in this match
            for player, payoff in zip(result.players, total_payoffs):
                if hasattr(player, 'attitude'):
                    if player.attitude == Attitude.COOPERATIVE:
                        cooperative_scores.append(payoff)
                    elif player.attitude == Attitude.AGGRESSIVE:
                        aggressive_scores.append(payoff)

        avg_coop = np.mean(cooperative_scores) if cooperative_scores else 0.0
        avg_agg = np.mean(aggressive_scores) if aggressive_scores else 0.0

        return avg_coop, avg_agg
