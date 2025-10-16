"""Batch tournament that runs mixture tournaments across different group sizes."""
import logging
from dataclasses import dataclass
from typing import Callable
import math
import pandas as pd
import numpy as np
from pathlib import Path

from emergent_llm.games.base_game import BaseGame
from emergent_llm.common import GameDescription, Attitude, Gene
from emergent_llm.players import BasePlayer, LLMPlayer, BaseStrategy, StrategySpec
from emergent_llm.tournament.configs import BatchTournamentConfig
from emergent_llm.tournament.mixture_tournament import MixtureTournament
from emergent_llm.tournament.base_tournament import BaseTournamentConfig
from emergent_llm.tournament.results import MixtureTournamentResults, BatchMixtureTournamentResults


class BatchMixtureTournament:
    """Tournament that runs mixture tournaments across multiple group sizes."""

    def __init__(self,
                 cooperative_strategies: list[StrategySpec],
                 aggressive_strategies: list[StrategySpec],
                 config: BatchTournamentConfig):

        self.cooperative_strategies = cooperative_strategies
        self.aggressive_strategies = aggressive_strategies
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialised multi-group tournament with {len(cooperative_strategies)} cooperative "
                        f"and {len(aggressive_strategies)} aggressive strategies")

        # Validate we have enough strategies for largest group size
        max_group_size = max(config.group_sizes)
        if len(cooperative_strategies) < max_group_size:
            raise ValueError(f"Need at least {max_group_size} cooperative players for largest group size, "
                           f"got {len(cooperative_strategies)}")
        if len(aggressive_strategies) < max_group_size:
            raise ValueError(f"Need at least {max_group_size} aggressive players for largest group size, "
                           f"got {len(aggressive_strategies)}")

        self.all_results: dict[int, MixtureTournamentResults] = {}

    def run_tournament(self) -> BatchMixtureTournamentResults:
        """Run tournaments across all group sizes."""
        for group_size in self.config.group_sizes:
            self.logger.info(f"Running tournament for group size {group_size}")

            # Generate game description for this group size
            game_description = self.config.game_description_generator(group_size)

            # Create mixture tournament config for this group size
            mixture_config = BaseTournamentConfig(
                game_description=game_description,
                repetitions=self.config.repetitions
            )

            cooperative_players = [spec.create_player(f"{spec.gene.attitude}_{i}", game_description)
                                   for i, spec in enumerate(self.cooperative_strategies)]
            aggressive_players  = [spec.create_player(f"{spec.gene.attitude}_{i}", game_description)
                                   for i, spec in enumerate(self.aggressive_strategies)]

            # Run mixture tournament for this group size
            mixture_tournament = MixtureTournament(
                cooperative_players=cooperative_players,
                aggressive_players=aggressive_players,
                config=mixture_config
            )

            result = mixture_tournament.run_tournament()
            self.all_results[group_size] = result

        return BatchMixtureTournamentResults(self.config, self.all_results)
