"""Cultural evolution tournament with genetic drift and selection."""
import logging
import random

from emergent_llm.common import Gene
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.players import LLMPlayer
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.configs import BaseTournamentConfig, CulturalEvolutionConfig
from emergent_llm.tournament.results import CulturalEvolutionResults


class CulturalEvolutionTournament:
    """Tournament simulating cultural evolution with selection and mutation."""

    def __init__(self,
                 config: CulturalEvolutionConfig,
                 strategy_registry: StrategyRegistry):
        """
        Initialize cultural evolution tournament.

        Args:
            config: Tournament configuration
            strategy_registry: Registry for sampling strategies from genes
        """
        self.config = config
        self.registry = strategy_registry
        self.logger = logging.getLogger(__name__)

        # Validate genes have strategies
        self.registry.validate_genes(config.genes)

        # Initialize population with uniform distribution over genes
        self.population: list[Gene] = []
        for i in range(config.population_size):
            gene = config.genes[i % len(config.genes)]
            self.population.append(gene)
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
        # Create players from current population
        players = self._create_players()

        # Run fair tournament
        fair_config = BaseTournamentConfig(
            game_description=self.config.game_description,
            repetitions=self.config.repetitions_per_generation
        )
        tournament = FairTournament(players, fair_config)
        results = tournament.run_tournament()
        self.generation_results.append(results)

        # Calculate fitness (mean payoff)
        fitnesses = [(player.gene, stats.mean_payoff)
                     for player, stats in zip(players, results.player_stats.values())]

        # Sort by fitness
        fitnesses.sort(key=lambda x: x[1], reverse=True)

        # Selection: keep top K
        survivors = [gene for gene, _ in fitnesses[:self.config.top_k]]

        # Reproduction: fill remaining slots
        fitness_values = [f for _, f in fitnesses]
        new_population = survivors.copy()

        while len(new_population) < self.config.population_size:
            # Fitness-proportional selection
            parent_gene = self._select_parent(fitnesses, fitness_values)

            # Mutation
            child_gene = self._mutate(parent_gene)
            new_population.append(child_gene)

        self.population = new_population

    def _create_players(self) -> list[LLMPlayer]:
        """Create player instances from current gene population."""
        players = []
        for i, gene in enumerate(self.population):
            strategy_class = self.registry.sample_strategy(gene)
            player = LLMPlayer(
                name=f"player_{i}",
                gene=gene,
                game_description=self.config.game_description,
                strategy_class=strategy_class
            )
            players.append(player)
        return players

    def _select_parent(self, fitnesses: list[tuple[Gene, float]],
                       fitness_values: list[float]) -> Gene:
        """Select parent using fitness-proportional selection."""
        # Handle negative fitnesses by shifting
        min_fitness = min(fitness_values)
        if min_fitness < 0:
            shifted_fitnesses = [f - min_fitness + 1 for f in fitness_values]
        else:
            shifted_fitnesses = fitness_values

        # Weighted random choice
        total_fitness = sum(shifted_fitnesses)
        if total_fitness == 0:
            # All equal fitness - uniform selection
            return random.choice([gene for gene, _ in fitnesses])

        r = random.uniform(0, total_fitness)
        cumulative = 0
        for (gene, _), shifted_fitness in zip(fitnesses, shifted_fitnesses):
            cumulative += shifted_fitness
            if r <= cumulative:
                return gene

        return fitnesses[-1][0]  # Fallback

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
        else:
            # Mutate attitude
            return Gene(gene.provider_model, gene.attitude.flip())

    def _calculate_gene_frequencies(self) -> dict[Gene, float]:
        """Calculate current gene frequencies."""
        counts = {}
        for gene in self.population:
            counts[gene] = counts.get(gene, 0) + 1

        return {gene: count / len(self.population)
                for gene, count in counts.items()}

    def _check_threshold(self, frequencies: dict[Gene, float]) -> bool:
        """Check if any gene has reached threshold."""
        return any(freq >= self.config.threshold_pct
                   for freq in frequencies.values())
