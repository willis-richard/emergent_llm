"""Cultural evolution tournament with genetic drift and selection."""
import logging
import random

import numpy as np
from emergent_llm.common import Gene
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.players import LLMPlayer, BaseStrategy, StrategySpec
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.configs import BaseTournamentConfig, CulturalEvolutionConfig
from emergent_llm.tournament.results import CulturalEvolutionResults


class CulturalEvolutionTournament:
    """Tournament simulating cultural evolution with selection and mutation."""

    def __init__(self,
                 config: CulturalEvolutionConfig,
                 strategy_registry: StrategyRegistry):
        """
        Initialise cultural evolution tournament.

        Args:
            config: Tournament configuration
            strategy_registry: Registry for sampling strategies from genes
        """
        self.config = config
        self.registry = strategy_registry
        self.logger = logging.getLogger(__name__)

        # Validate genes have strategies
        self.registry.validate_genes(config.genes)

        # Initialise with uniform distribution over genes
        self.population: list[StrategySpec] = []
        for i in range(config.population_size):
            gene = config.genes[i % len(config.genes)]
            spec = self.registry.sample_spec(gene)
            self.population.append(spec)
        random.shuffle(self.population)

        # Track history
        self.generation = 0
        self.gene_frequencies: list[dict[Gene, float]] = []
        self.generation_results: list = []

    def run_tournament(self) -> CulturalEvolutionResults:
        """Run cultural evolution until termination condition met."""
        self.logger.info(f"Starting cultural evolution with {self.config.population_size} players")

        while self.generation < self.config.max_generations:
            self.logger.info(f"Generation {self.generation}")

            # Record gene frequencies
            frequencies = self._calculate_gene_frequencies()
            self.gene_frequencies.append(frequencies)
            self.logger.info(f"Gene frequencies: {frequencies}")

            # Check termination
            if self._check_threshold(frequencies):
                self.logger.info("Threshold reached - terminating")
                break

            # Run generation
            self._run_generation()
            self.generation += 1

        # Final frequency calculation
        final_frequencies = self._calculate_gene_frequencies()
        self.gene_frequencies.append(final_frequencies)

        return CulturalEvolutionResults(
            config=self.config,
            final_generation=self.generation,
            final_gene_frequencies=final_frequencies,
            gene_frequency_history=self.gene_frequencies,
            generation_results=self.generation_results
        )

    def _run_generation(self):
        """Run one generation: compete, select, reproduce."""
        # Create players from current population (using existing strategies)
        players = [spec.create_player(f"player_{i}", self.config.game_description)
                   for i, spec in enumerate(self.population)]

        # Run fair tournament
        fair_config = BaseTournamentConfig(
            game_description=self.config.game_description,
            repetitions=self.config.repetitions_per_generation
        )
        tournament = FairTournament(players, fair_config)
        results = tournament.run_tournament()
        self.generation_results.append(results)

        # Calculate fitness array (mean payoff)
        fitnesses = np.array([stats.mean_payoff for stats in results.player_stats.values()])

        # Get indices sorted by fitness (descending)
        sorted_indices = np.argsort(fitnesses)[::-1]

        # Selection: keep top K individuals
        survivor_indices = sorted_indices[:self.config.top_k]
        survivors = [self.population[i] for i in survivor_indices]

        # Reproduction: vectorized offspring generation
        n_offspring = self.config.population_size - self.config.top_k
        offspring = self._create_offspring(fitnesses, n_offspring)

        self.population = survivors + offspring

    def _create_offspring(self,
                         fitnesses: np.ndarray,
                         n_offspring: int) -> list[StrategySpec]:
        """
        Create offspring via fitness-proportional selection and mutation.

        Args:
            fitnesses: Array of fitness values (aligned with self.population by index)
            n_offspring: Number of offspring to create

        Returns:
            List of StrategySpec for offspring
        """
        # Fitness-proportional probabilities
        # Games must have at least one player having positive payoffs, and no negative payoffs
        # so there are no division by zero or negative issues
        probabilities = fitnesses / fitnesses.sum()

        # Sample parents (with replacement)
        parent_indices = np.random.choice(len(self.population), size=n_offspring, p=probabilities)

        # Create offspring
        offspring: list[StrategySpec] = []
        for idx in parent_indices:
            parent_gene, _ = self.population[idx]

            # Mutation
            child_gene = self._mutate(parent_gene)

            # Sample new strategy for child
            child_spec = self.registry.sample_spec(child_gene)

            offspring.append(child_spec)

        return offspring

    def _mutate(self, gene: Gene) -> Gene:
        """Apply mutation to gene."""
        if random.random() >= self.config.mutation_rate:
            return gene  # No mutation

        # 50/50 chance of mutating provider_model vs attitude
        available_models = self.registry.available_provider_models

        if random.random() < 0.5 and len(available_models) > 1:
            # Mutate provider_model
            other_models = available_models - {gene.provider_model}
            new_provider = random.choice(list(other_models))
            return Gene(new_provider, gene.attitude)

        # Mutate attitude
        return Gene(gene.provider_model, gene.attitude.flip())

    def _calculate_gene_frequencies(self) -> dict[Gene, float]:
        """Calculate current gene frequencies."""
        counts: dict[Gene, float] = {}
        for individual in self.population:
            counts[individual.gene] = counts.get(individual.gene, 0) + 1

        return {gene: count / len(self.population)
                for gene, count in counts.items()}

    def _check_threshold(self, frequencies: dict[Gene, float]) -> bool:
        """Check if any gene has reached threshold."""
        return any(freq >= self.config.threshold_pct
                   for freq in frequencies.values())
