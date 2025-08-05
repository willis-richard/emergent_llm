"""Multi-group tournament that runs mixture tournaments across different group sizes."""
import logging
from dataclasses import dataclass
from typing import List, Callable
import pandas as pd
import numpy as np

from emergent_llm.games.base_game import BaseGame
from emergent_llm.common import GameDescription
from emergent_llm.players import BasePlayer
from emergent_llm.tournament.mixture_tournament import MixtureTournament, MixtureTournamentConfig


@dataclass
class MultiGroupTournamentConfig:
    """Configuration for multi-group tournament."""
    game_class: type[BaseGame]
    group_sizes: List[int]
    matches_per_mixture: int
    output_prefix: str
    game_description_generator: Callable[[int], GameDescription]  # Just takes group_size, returns GameDescription


class MultiGroupTournament:
    """Tournament that runs mixture tournaments across multiple group sizes."""

    def __init__(self,
                 cooperative_players: List[BasePlayer],
                 aggressive_players: List[BasePlayer],
                 config: MultiGroupTournamentConfig):

        self.cooperative_players = cooperative_players
        self.aggressive_players = aggressive_players
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized multi-group tournament with {len(cooperative_players)} cooperative "
                        f"and {len(aggressive_players)} aggressive players")

        # Validate we have enough strategies for largest group size
        max_group_size = max(config.group_sizes)
        if len(cooperative_players) < max_group_size:
            raise ValueError(f"Need at least {max_group_size} cooperative players for largest group size, "
                           f"got {len(cooperative_players)}")
        if len(aggressive_players) < max_group_size:
            raise ValueError(f"Need at least {max_group_size} aggressive players for largest group size, "
                           f"got {len(aggressive_players)}")

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

            # Run mixture tournament for this group size
            mixture_tournament = MixtureTournament(
                cooperative_players=self.cooperative_players,
                aggressive_players=self.aggressive_players,
                config=mixture_config
            )

            results_df = mixture_tournament.run_tournament()
            self.all_results.append(results_df)

            # Generate Schelling diagram for this group size
            output_path = f'{self.config.output_prefix}_schelling_n{group_size}'
            mixture_tournament.create_schelling_diagram(output_path)

        # Combine all results and create summary table
        combined_results = pd.concat(self.all_results, ignore_index=True)
        self._create_summary_table(combined_results)

        return combined_results

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

        # Save to CSV
        output_file = f'{self.config.output_prefix}_summary_table.csv'
        pivot_df.to_csv(output_file)

        self.logger.info(f"Summary table saved: {output_file}")

        # Also print to console
        print("\n=== SOCIAL WELFARE SUMMARY TABLE ===")
        print("Rows: Aggressive player ratio, Columns: Group size")
        print(pivot_df.to_string(float_format='%.3f'))

        # Print some debug info
        print(f"\nMatches played per mixture: {self.config.matches_per_mixture}")
        print(f"Group sizes tested: {self.config.group_sizes}")
