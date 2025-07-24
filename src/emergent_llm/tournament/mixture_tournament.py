"""Mixture tournament testing different ratios of cooperative vs aggressive players."""
import logging
import random
from typing import List
import pandas as pd
import numpy as np
from pathlib import Path

from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.games.base_game import BaseGame, GameDescription
from emergent_llm.players.players import LLMPlayer
from emergent_llm.common.attitudes import Attitude


class MixtureTournament(FairTournament):
    """Tournament testing different mixtures of cooperative vs aggressive players."""

    def __init__(self, cooperative_strategies: List[type],
                 aggressive_strategies: List[type],
                 game_class: type[BaseGame],
                 game_description: GameDescription,
                 matches_per_mixture: int = 100,
                 verbose_logging: bool = False,
                 log_file: str = None):

        # We'll override the players, so just pass empty list to parent
        super().__init__([], game_class, game_description)

        self.cooperative_strategies = cooperative_strategies
        self.aggressive_strategies = aggressive_strategies
        self.matches_per_mixture = matches_per_mixture
        self.verbose_logging = verbose_logging

        # Setup file logging if requested
        if log_file:
            self._setup_file_logging(log_file)

        self.logger.info(f"Mixture tournament: {len(cooperative_strategies)} cooperative, "
                        f"{len(aggressive_strategies)} aggressive strategies")

    def _setup_file_logging(self, log_file: str):
        """Add file logging to existing logger."""
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, mode='w')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.info(f"File logging enabled: {log_path}")

    def run_mixture_tournament(self) -> pd.DataFrame:
        """Run tournament testing all mixtures."""
        results = []

        self.logger.info("Starting mixture tournament")

        for n_aggressive in range(self.game_description.n_players + 1):
            n_cooperative = self.game_description.n_players - n_aggressive

            self.logger.info(f"\nTesting mixture: {n_cooperative}C + {n_aggressive}A")

            # Run matches for this mixture
            mixture_results = self._run_mixture(n_cooperative, n_aggressive)

            # Calculate averages
            avg_coop, avg_agg = self._calculate_mixture_averages(mixture_results, n_cooperative)

            results.append({
                'n_cooperative': n_cooperative,
                'n_aggressive': n_aggressive,
                'ratio_aggressive': n_aggressive / self.game_description.n_players,
                'avg_cooperative_score': avg_coop,
                'avg_aggressive_score': avg_agg,
                'n_matches': len(mixture_results)
            })

            self.logger.info(f"Mixture complete. Coop avg: {avg_coop:.3f}, Agg avg: {avg_agg:.3f}")

        return pd.DataFrame(results)

    def _run_mixture(self, n_cooperative: int, n_aggressive: int):
        """Run all matches for a specific mixture."""
        match_results = []

        for match_num in range(self.matches_per_mixture):
            match_id = f"mix_{n_cooperative}c_{n_aggressive}a_match_{match_num:03d}"

            # Create players for this match
            players = self._create_match_players(n_cooperative, n_aggressive, match_num)

            try:
                # Run the game
                game = self.game_class(players, self.game_description)
                result = game.play_game()
                match_results.append(result)

                # Log match details if verbose
                if self.verbose_logging:
                    result.log_match_result(match_id, self.logger)
                else:
                    # Just log basic match info
                    total_payoffs = result.history.payoffs.sum(axis=0)
                    scores = [f"P{i}:{score:.2f}" for i, score in enumerate(total_payoffs)]
                    self.logger.info(f"{match_id} - Scores: {', '.join(scores)}")

            except Exception as e:
                self.logger.error(f"Error in {match_id}: {e}")
                continue

        return match_results

    def _create_match_players(self, n_cooperative: int, n_aggressive: int, match_num: int) -> List[LLMPlayer]:
        """Create players for a single match."""
        players = []

        # Cooperative players
        for i in range(n_cooperative):
            strategy_class = random.choice(self.cooperative_strategies)
            player = LLMPlayer(f"coop_m{match_num}_p{i}", Attitude.COOPERATIVE,
                             self.game_description, strategy_class)
            players.append(player)

        # Aggressive players
        for i in range(n_aggressive):
            strategy_class = random.choice(self.aggressive_strategies)
            player = LLMPlayer(f"agg_m{match_num}_p{i}", Attitude.AGGRESSIVE,
                             self.game_description, strategy_class)
            players.append(player)

        # Shuffle to randomize positions
        random.shuffle(players)
        return players

    def _calculate_mixture_averages(self, mixture_results, n_cooperative: int):
        """Calculate average scores by player type."""
        cooperative_scores = []
        aggressive_scores = []

        for result in mixture_results:
            total_payoffs = result.history.payoffs.sum(axis=0)

            # Identify cooperative vs aggressive players by their names
            for i, (player_name, payoff) in enumerate(zip(result.players, total_payoffs)):
                if "coop_" in player_name:
                    cooperative_scores.append(payoff)
                elif "agg_" in player_name:
                    aggressive_scores.append(payoff)

        avg_coop = np.mean(cooperative_scores) if cooperative_scores else 0.0
        avg_agg = np.mean(aggressive_scores) if aggressive_scores else 0.0

        return avg_coop, avg_agg

    def print_summary(self, results_df: pd.DataFrame):
        """Print a summary of tournament results."""
        print(f"\n{'='*60}")
        print(f"MIXTURE TOURNAMENT RESULTS")
        print(f"{'='*60}")
        print(f"Game: {self.game_description.__class__.__name__}")
        print(f"Players per game: {self.game_description.n_players}")
        print(f"Matches per mixture: {self.matches_per_mixture}")
        print(f"{'='*60}")

        for _, row in results_df.iterrows():
            n_coop = int(row['n_cooperative'])
            n_agg = int(row['n_aggressive'])
            print(f"Mixture: {n_coop}C + {n_agg}A")

            if n_coop > 0:
                print(f"  Avg Cooperative Score: {row['avg_cooperative_score']:.3f}")
            if n_agg > 0:
                print(f"  Avg Aggressive Score:   {row['avg_aggressive_score']:.3f}")
            print()
