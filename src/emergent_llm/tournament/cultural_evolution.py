"""Cultural evolution tournament with genetic drift and selection."""
import logging
import random
from collections import Counter
from math import ceil

import numpy as np

from emergent_llm.common import Gene, Attitude
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.players import BaseStrategy, LLMPlayer, StrategySpec
from emergent_llm.tournament.configs import BaseTournamentConfig, CulturalEvolutionConfig, SurvivorRecord
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.results import CulturalEvolutionResults


class CulturalEvolution:
    """Simulate cultural evolution with selection and mutation."""

    def __init__(self, config: CulturalEvolutionConfig,
                 strategy_registry: StrategyRegistry):
        """
        Initialise cultural evolution tournament.

        Args:
            config:  CulturalEvolution tournament config
            strategy_registry: Registry for sampling strategies from genes
        """
        self.config = config
        self.registry = strategy_registry
        self.logger = logging.getLogger(__name__)

        # Validate all model+attitude combinations exist
        for model in self.registry.available_models:
            for attitude in [Attitude.COLLECTIVE, Attitude.EXPLOITATIVE]:
                gene = Gene(model, attitude)
                if gene not in self.registry.available_genes:
                    raise ValueError(f"Missing strategies for {gene}")

        self.reset()

    def initialise_population(self):
        genes = self.registry.available_genes

        # Initialise with uniform distribution over genes
        self.population = [
            self.registry.sample_spec(gene)
            for gene in genes
            for _ in range(ceil(self.config.population_size / len(genes)))
        ]
        random.shuffle(self.population)
        self.population = self.population[:self.config.population_size]

        self.logger.debug(f"Population\n" +
                          "\n".join(map(str, self.population)))

    def reset(self):
        self.generation = 0
        self.gene_frequencies: list[dict[Gene, float]] = []
        self.generation_results: list = []
        self.survivor_history: list[list[SurvivorRecord]] = []
        self.initialise_population()

    def run_tournament(self) -> CulturalEvolutionResults:
        """Run cultural evolution until termination condition met."""
        self.logger.info(
            f"Starting cultural evolution with {self.config.population_size} players"
        )

        while self.generation < self.config.max_generations:
            self.logger.info(f"Generation {self.generation}")

            # Record gene frequencies
            frequencies = self._calculate_gene_frequencies()
            self.gene_frequencies.append(frequencies)
            freq_str = ", ".join(
                f"{gene}: {freq:.2%}" for gene, freq in frequencies.items())
            self.logger.info(f"Gene frequencies: {freq_str}")

            # Check termination
            if self._check_threshold(frequencies):
                self.logger.info("Threshold reached - terminating")
                break

            # Run generation
            self._run_generation()
            self.generation += 1
        else:
            # Final frequency calculation if we exited via max generations
            frequencies = self._calculate_gene_frequencies()
            self.gene_frequencies.append(frequencies)

        return CulturalEvolutionResults(
            config=self.config,
            final_generation=self.generation,
            final_gene_frequencies=frequencies,
            gene_frequency_history=self.gene_frequencies,
            generation_results=self.generation_results,
            survivor_history=self.survivor_history)

    def _run_generation(self):
        """Run one generation: compete, select, reproduce."""
        # Create players from current population (using existing strategies)
        players = [
            spec.create_player(f"player_{i}", self.config.game_description)
            for i, spec in enumerate(self.population)
        ]
        self.logger.debug(f"Players created:\n" + "\n".join(map(str, players)))

        # Run fair tournament
        fair_config = BaseTournamentConfig(
            game_description=self.config.game_description,
            repetitions=self.config.repetitions_per_generation)
        tournament = FairTournament(players, fair_config)
        results = tournament.run_tournament()
        self.generation_results.append(results)
        self.logger.debug(results.results_df)

        # Calculate fitness array (mean payoff)
        player_scores = results.results_df.set_index(
            'player_name')['mean_payoff'].to_dict()
        fitnesses = np.array([player_scores[p.id.name] for p in players])
        self.logger.debug(f"Fitnesses: {fitnesses}")

        # Selection: keep top K by argsort (already efficient)
        survivor_indices = np.argsort(fitnesses)[-self.config.top_k:]
        survivors = [self.population[i] for i in survivor_indices]
        survivor_fitnesses = fitnesses[survivor_indices]
        self.logger.debug(f"Survivors:\n" + "\n".join(map(str, survivors)))

        # Record survivors
        survivor_records = [
            SurvivorRecord(
                gene=spec.gene,
                strategy_name=spec.strategy_class.__name__,
                fitness=float(fitness)
            )
            for spec, fitness in zip(survivors, survivor_fitnesses)
        ]
        self.survivor_history.append(survivor_records)

        self.logger.debug(f"Survivors:\n" + "\n".join(
            f"{r.strategy_name} ({r.gene}): {r.fitness:.2f}" for r in survivor_records
        ))

        # Reproduction
        n_offspring = self.config.population_size - self.config.top_k
        offspring = self._create_offspring(fitnesses, n_offspring)
        self.logger.debug(f"Offspring:\n" + "\n".join(map(str, offspring)))

        self.population = survivors + offspring

    def _create_offspring(self, fitnesses: np.ndarray,
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
        self.logger.debug(f"Probabilities: {probabilities}")

        # Sample parents (with replacement)
        parent_indices = np.random.choice(len(self.population),
                                          size=n_offspring,
                                          p=probabilities)
        self.logger.debug(f"Parent indices: {parent_indices}")

        # Create offspring
        offspring: list[StrategySpec] = []
        for idx in parent_indices:
            parent_gene = self.population[idx].gene

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

        # 50/50 chance of mutating model vs attitude
        available_models = self.registry.available_models

        if random.random() < 0.5 and len(available_models) > 1:
            # Mutate model
            other_models = available_models - {gene.model}
            new_model = random.choice(list(other_models))
            return Gene(new_model, gene.attitude)

        # Mutate attitude
        return Gene(gene.model, gene.attitude.flip())

    def _calculate_gene_frequencies(self) -> dict[Gene, float]:
        """Calculate current gene frequencies in descending order."""
        gene_counts = Counter(spec.gene for spec in self.population)
        total = len(self.population)
        # Return as sorted dict
        return dict(
            sorted(
                ((gene, count / total) for gene, count in gene_counts.items()),
                key=lambda x: x[1],
                reverse=True))

    def _check_threshold(self, frequencies: dict[Gene, float]) -> bool:
        """Check if any gene has reached threshold."""
        return any(
            freq >= self.config.threshold_pct for freq in frequencies.values())
