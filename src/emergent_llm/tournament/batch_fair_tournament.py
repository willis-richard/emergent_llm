"""Multi-group fair tournament for testing strategy generalization across group sizes."""
import logging
from dataclasses import dataclass
from typing import Callable
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from emergent_llm.games.base_game import BaseGame
from emergent_llm.common import GameDescription, Attitude
from emergent_llm.players import BasePlayer, LLMPlayer, BaseStrategy
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.base_tournament import BaseTournamentConfig


@dataclass
class BatchFairTournamentConfig:
    """Configuration for multi-group fair tournament."""
    group_sizes: list[int]
    repetitions: int
    results_dir: str
    game_description_generator: Callable[[int], GameDescription]
    population_multiplier: int = 4  # Population = max_group_size * this


class BatchFairTournament:
    """Tournament that tests strategy generalization across multiple group sizes."""

    def __init__(self,
                 cooperative_strategies: list[type[BaseStrategy]],
                 aggressive_strategies: list[type[BaseStrategy]],
                 config: BatchFairTournamentConfig):

        self.cooperative_strategies = cooperative_strategies
        self.aggressive_strategies = aggressive_strategies
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)
        n_strategies = len(cooperative_strategies) + len(aggressive_strategies)
        self.logger.info(f"Initialised batch fair tournament with {n_strategies} strategies")

        # Validate we have enough strategies for largest group size with population multiplier
        max_group_size = max(config.group_sizes)
        required_population = max_group_size * config.population_multiplier

        if n_strategies < required_population:
            raise ValueError(
                f"Need at least {required_population} strategies for largest group size "
                f"({max_group_size}) with population multiplier ({config.population_multiplier}), "
                f"got {n_strategies}"
            )

        # Storage for all results
        self.all_results: list[pd.DataFrame] = []

    def run_tournament(self) -> pd.DataFrame:
        """Run fair tournaments across all group sizes."""
        for group_size in tqdm(self.config.group_sizes, desc="Group sizes"):
            self.logger.info(f"Running fair tournament for group size {group_size}")

            # Generate game description for this group size
            game_description = self.config.game_description_generator(group_size)

            # Create tournament config for this group size
            tournament_config = BaseTournamentConfig(
                game_description=game_description,
                repetitions=self.config.repetitions
            )

            players = self.create_players_from_strategies(game_description)

            # Run fair tournament for this group size
            fair_tournament = FairTournament(players, tournament_config)
            results_df = fair_tournament.run_tournament()

            # Add group size information
            results_df['group_size'] = group_size
            self.all_results.append(results_df)

            # Save individual results
            self._save_group_results(results_df, group_size)

        # Combine all results and create analysis
        combined_results = pd.concat(self.all_results, ignore_index=True)
        self._create_generalization_analysis(combined_results)

        return combined_results

    def create_players_from_strategies(self, game_description: GameDescription) -> list[BasePlayer]:
        """Create player instances from strategy classes."""
        players = []

        for i, strategy_class in enumerate(self.cooperative_strategies):
            player = LLMPlayer(f"coop_{strategy_class.__name__}",
                            Attitude.COOPERATIVE,
                            game_description,  # Just for initialization
                            strategy_class)
            players.append(player)

        for i, strategy_class in enumerate(self.aggressive_strategies):
            player = LLMPlayer(f"agg_{strategy_class.__name__}",
                            Attitude.AGGRESSIVE,
                            game_description,  # Just for initialization
                            strategy_class)
            players.append(player)

        return players

    def _save_group_results(self, results_df: pd.DataFrame, group_size: int):
        """Save results for a specific group size."""
        output_dir = Path(self.config.results_dir) / "group_results"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"group_size_{group_size}.csv"
        results_df.to_csv(output_file, index=False)

        self.logger.info(f"Group {group_size} results saved: {output_file}")

    def _create_generalization_analysis(self, results_df: pd.DataFrame):
        """Create analysis of how strategies generalize across group sizes."""
        output_dir = Path(self.config.results_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Save combined results
        combined_file = output_dir / "combined_results.csv"
        results_df.to_csv(combined_file, index=False)

        # 2. Create generalization summary
        generalization_summary = self._create_generalization_summary(results_df)
        summary_file = output_dir / "generalization_summary.csv"
        generalization_summary.to_csv(summary_file, index=False)

        # 3. Create ranking consistency analysis
        ranking_consistency = self._analyze_ranking_consistency(results_df)
        ranking_file = output_dir / "ranking_consistency.csv"
        ranking_consistency.to_csv(ranking_file, index=False)

        self.logger.info(f"Analysis files saved to {output_dir}")

        # Print summary to console
        print("\n=== GENERALIZATION ANALYSIS ===")
        print(f"Tested group sizes: {self.config.group_sizes}")
        print("\nTop strategies by overall performance:")
        print(generalization_summary.head(10).to_string(index=False, float_format='%.3f'))

    def _create_generalization_summary(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Create summary of strategy performance across group sizes."""
        # Extract strategy name from player_name (remove instance suffix)
        results_df['strategy_name'] = results_df['player_name'].str.rsplit('_', n=1).str[0]

        # Group by strategy and group size, then calculate mean performance
        strategy_performance = results_df.groupby(['strategy_name', 'group_size']).agg({
            'mean_payoff': 'mean',
            'mean_cooperations': 'mean',
            'games_played': 'sum'
        }).reset_index()

        # Calculate overall statistics per strategy
        overall_stats = strategy_performance.groupby('strategy_name').agg({
            'mean_payoff': ['mean', 'std'],
            'mean_cooperations': ['mean', 'std']
        }).round(4)

        # Flatten column names
        overall_stats.columns = ['_'.join(col).strip() for col in overall_stats.columns]
        overall_stats = overall_stats.reset_index()

        # Sort by overall mean payoff
        return overall_stats.sort_values('mean_payoff_mean', ascending=False)

    def _analyze_ranking_consistency(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Analyze how consistent strategy rankings are across group sizes."""
        # Extract strategy name
        results_df['strategy_name'] = results_df['player_name'].str.rsplit('_', n=1).str[0]

        rankings = []

        for group_size in self.config.group_sizes:
            group_data = results_df[results_df['group_size'] == group_size]

            # Get mean performance per strategy for this group size
            strategy_means = group_data.groupby('strategy_name')['mean_payoff'].mean()
            strategy_ranks = strategy_means.rank(ascending=False, method='average')

            for strategy, rank in strategy_ranks.items():
                rankings.append({
                    'strategy_name': strategy,
                    'group_size': group_size,
                    'rank': rank,
                    'mean_payoff': strategy_means[strategy]
                })

        rankings_df = pd.DataFrame(rankings)

        # Calculate ranking consistency (standard deviation of ranks)
        consistency = rankings_df.groupby('strategy_name')['rank'].agg(['mean', 'std']).round(2)
        consistency.columns = ['mean_rank', 'rank_std']
        consistency = consistency.sort_values('mean_rank').reset_index()

        return consistency
