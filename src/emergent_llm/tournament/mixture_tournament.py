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

    def run_mixture_tournament(self) -> pd.DataFrame:
        """Run tournament testing different mixtures of cooperative vs aggressive players."""
        n_players = self.game_description.n_players
        all_results = []

        # Test different mixtures from all cooperative to all aggressive
        for n_cooperative in range(n_players + 1):
            n_aggressive = n_players - n_cooperative

            # Skip invalid mixtures
            if n_cooperative > len(self.cooperative_players) or n_aggressive > len(self.aggressive_players):
                continue

            self.logger.info(f"Testing mixture: {n_cooperative} cooperative, {n_aggressive} aggressive")

            mixture_results = []
            mixture_players_used = []  # Track actual players for each match

            # Run multiple matches for this mixture
            for match_num in range(self.matches_per_mixture):
                try:
                    # Create players for this match
                    match_players = self._create_match_players(n_cooperative, n_aggressive, match_num)
                    mixture_players_used.append(match_players)  # Store for later analysis

                    # Run the match
                    match_id = f"mixture_{n_cooperative}c_{n_aggressive}a_match_{match_num:03d}"
                    result = self._run_match(match_players, match_id)
                    mixture_results.append(result)

                except Exception as e:
                    self.logger.error(f"Error in match {match_id}: {e}")
                    continue

            # Calculate averages for this mixture
            avg_coop, avg_agg = self._calculate_mixture_averages(mixture_results, mixture_players_used)

            # Add summary row
            all_results.append({
                'n_cooperative': n_cooperative,
                'n_aggressive': n_aggressive,
                'avg_cooperative_score': avg_coop,
                'avg_aggressive_score': avg_agg,
                'matches_played': len(mixture_results)
            })

        return pd.DataFrame(all_results)

    def _calculate_mixture_averages(self, mixture_results, mixture_players_used):
        """Calculate average scores by player type using stored player references."""
        cooperative_scores = []
        aggressive_scores = []

        for result, players_used in zip(mixture_results, mixture_players_used):
            total_payoffs = result.game_result.history.payoffs.sum(axis=0)

            for player, payoff in zip(players_used, total_payoffs):
                if hasattr(player, 'attitude'):
                    if player.attitude == Attitude.COOPERATIVE:
                        cooperative_scores.append(payoff)
                    elif player.attitude == Attitude.AGGRESSIVE:
                        aggressive_scores.append(payoff)

        avg_coop = np.mean(cooperative_scores) if cooperative_scores else 0.0
        avg_agg = np.mean(aggressive_scores) if aggressive_scores else 0.0

        return avg_coop, avg_agg


    def print_summary(self, results_df: pd.DataFrame):
        """Print summary of mixture tournament results."""
        print("\n=== MIXTURE TOURNAMENT RESULTS ===")
        print(results_df.to_string(index=False, float_format='%.3f'))
