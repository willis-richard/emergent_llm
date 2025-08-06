"""Multi-group tournament that runs mixture tournaments across different group sizes."""
import logging
from dataclasses import dataclass
from typing import List, Callable
import pandas as pd
import numpy as np
from pathlib import Path

from emergent_llm.games.base_game import BaseGame
from emergent_llm.common import GameDescription, Attitude
from emergent_llm.players import BasePlayer, LLMPlayer, BaseStrategy
from emergent_llm.tournament.mixture_tournament import MixtureTournament, MixtureTournamentConfig


@dataclass
class MultiGroupTournamentConfig:
    """Configuration for multi-group tournament."""
    game_class: type[BaseGame]
    group_sizes: List[int]
    matches_per_mixture: int
    results_dir: str
    game_description_generator: Callable[[int], GameDescription]  # Just takes group_size, returns GameDescription


class MultiGroupTournament:
    """Tournament that runs mixture tournaments across multiple group sizes."""

    def __init__(self,
                 cooperative_strategies: List[BaseStrategy],
                 aggressive_strategies: List[BaseStrategy],
                 config: MultiGroupTournamentConfig):

        self.cooperative_strategies = cooperative_strategies
        self.aggressive_strategies = aggressive_strategies
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized multi-group tournament with {len(cooperative_strategies)} cooperative "
                        f"and {len(aggressive_strategies)} aggressive strategies")

        # Validate we have enough strategies for largest group size
        max_group_size = max(config.group_sizes)
        if len(cooperative_strategies) < max_group_size:
            raise ValueError(f"Need at least {max_group_size} cooperative players for largest group size, "
                           f"got {len(cooperative_strategies)}")
        if len(aggressive_strategies) < max_group_size:
            raise ValueError(f"Need at least {max_group_size} aggressive players for largest group size, "
                           f"got {len(aggressive_strategies)}")

        # Storage for all results
        self.all_results: List[pd.DataFrame] = []

    def run_tournament(self) -> pd.DataFrame:
        """Run tournaments across all group sizes."""
        for group_size in self.config.group_sizes:
            self.logger.info(f"Running tournament for group size {group_size}")

            # Generate game description for this group size
            game_description = self.config.game_description_generator(group_size)

            # Create mixture tournament config for this group size
            mixture_config = MixtureTournamentConfig(
                game_class=self.config.game_class,
                game_description=game_description,
                matches_per_mixture=self.config.matches_per_mixture
            )

            # Create players
            cooperative_players, aggressive_players = self.create_players_from_strategies(game_description)

            # Run mixture tournament for this group size
            mixture_tournament = MixtureTournament(
                cooperative_players=cooperative_players,
                aggressive_players=aggressive_players,
                config=mixture_config
            )

            results_df = mixture_tournament.run_tournament()
            self.all_results.append(results_df)

            # Generate Schelling diagram for this group size
            output_path = f'{self.config.results_dir}/schelling/n_{group_size}'
            mixture_tournament.create_schelling_diagram(output_path)

        # Combine all results and create summary table
        combined_results = pd.concat(self.all_results, ignore_index=True)
        self._create_summary_table(combined_results)

        return combined_results

    def create_players_from_strategies(self, game_description):
        """Create player instances from strategy classes."""
        cooperative_players = []
        aggressive_players = []

        for i, strategy_class in enumerate(self.cooperative_strategies):
            player = LLMPlayer(f"coop_{strategy_class.__name__}",
                            Attitude.COOPERATIVE,
                            game_description,  # Just for initialization
                            strategy_class)
            cooperative_players.append(player)

        for i, strategy_class in enumerate(self.aggressive_strategies):
            player = LLMPlayer(f"agg_{strategy_class.__name__}",
                            Attitude.AGGRESSIVE,
                            game_description,  # Just for initialization
                            strategy_class)
            aggressive_players.append(player)

        return cooperative_players, aggressive_players

    def _create_summary_table(self, results_df: pd.DataFrame):
        """Create summary table with social welfare across group sizes and ratios."""
        # Create pivot table with aggressive ratios as rows and group sizes as columns
        pivot_df = results_df.pivot_table(
            values='avg_social_welfare',
            index='aggressive_ratio',
            columns='group_size',
            fill_value=np.nan
        )

        # Format as percentages for the index
        pivot_df.index = [f"{ratio:.0%}" for ratio in pivot_df.index]

        # Save to CSV using the main output prefix
        output_file = f'{self.config.results_dir}/summary_table.csv'
        pivot_df.to_csv(output_file)

        self.logger.info(f"Summary table saved: {output_file}")

        # Also print to console
        print("\n=== SOCIAL WELFARE SUMMARY TABLE ===")
        print("Rows: Aggressive player ratio, Columns: Group size")
        print(pivot_df.to_string(float_format='%.3f'))

        # Print some debug info
        print(f"\nMatches played per mixture: {self.config.matches_per_mixture}")
        print(f"Group sizes tested: {self.config.group_sizes}")
