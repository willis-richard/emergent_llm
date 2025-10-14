"""Evolutionary tournament with cultural evolution dynamics."""
import logging
import random
from dataclasses import dataclass, field
from typing import Callable

from emergent_llm.common import Attitude, GameDescription
from emergent_llm.players import LLMPlayer
from emergent_llm.tournament.configs import BaseTournamentConfig
from emergent_llm.tournament.evolutionary_player import (
    EvolutionaryPlayer, Gene, PlayerDatabase, PlayerFactory, StrategyRegistry
)
from emergent_llm.tournament.fair_tournament import FairTournament


@dataclass
class GenerationSnapshot:
    """Snapshot of evolutionary state at a single generation."""
    generation: int
    gene_frequencies: dict[Gene, int]  # gene -> count
    attitude_frequencies: dict[Attitude, int]
    provider_frequencies: dict[str, int]
    mean_fitness: float
    max_fitness: float
    min_fitness: float
    elite_player_ids: list[int]  # IDs of elite players


@dataclass
class EvolutionaryConfig:
    """Configuration for evolutionary tournament."""
    population_size: int
    max_generations: int
    n_elite: int
    mutation_rate: float
    n_convergenced: int  # Stop when a gene reaches this count
    game_description: GameDescription
    repetitions: int = 1  # Repetitions per FairTournament

    def __post_init__(self):
        """Validate configuration."""
        if self.population_size % self.game_description.n_players != 0:
            raise ValueError(
                f"population_size ({self.population_size}) must be divisible by "
                f"n_players ({self.game_description.n_players})"
            )
        if self.n_elite >= self.population_size:
            raise ValueError("n_elite must be less than population_size")
        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("mutation_rate must be between 0 and 1")
        if not 0 < self.convergence_threshold <= 1:
            raise ValueError("convergence_threshold must be between 0 and 1")


class EvolutionaryTournament:
    """Tournament implementing cultural evolution with success-biased learning."""

    def __init__(self,
                 strategy_registry: StrategyRegistry,
                 config: EvolutionaryConfig):
        self.registry = strategy_registry
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create database and factory
        self.database = PlayerDatabase()
        self.factory = PlayerFactory(
            database=self.database,
            registry=strategy_registry,
            mutation_rate=config.mutation_rate
        )

        # Get available provider models for mutations
        self.available_provider_models = list(set(
            gene.provider_model for gene in strategy_registry.available_genes()
        ))

        # Initialize population and tracking
        self.population: list[EvolutionaryPlayer] = []
        self.generation_snapshots: list[GenerationSnapshot] = []

    def run_evolution(self):
        """Run evolutionary tournament until convergence or max generations."""
        # Create initial population
        self.population = self._create_initial_population()
        self.logger.info(f"Created initial population of {len(self.population)} players")

        gen = 0
        while True:
            self.logger.info(f"Running generation {gen}")

            # Run tournament for this generation
            self._run_generation_tournament()

            # Record snapshot
            snapshot = self._record_snapshot(gen)
            self.generation_snapshots.append(snapshot)

            # Log progress
            dominant_gene = max(snapshot.gene_frequencies, key=snapshot.gene_frequencies.get)
            dominant_freq = snapshot.gene_frequencies[dominant_gene] / self.config.population_size
            self.logger.info(
                f"Gen {gen}: dominant gene {dominant_gene} at {dominant_freq:.2%}, "
                f"mean fitness {snapshot.mean_fitness:.2f}"
            )

            # Check stopping criteria
            convergence_reason = self._check_stopping(gen, snapshot)
            if convergence_reason:
                self.logger.info(f"Stopping: {convergence_reason}")
                return EvolutionaryResults(
                    config=self.config,
                    generation_snapshots=self.generation_snapshots,
                    final_generation=gen,
                    convergence_reason=convergence_reason,
                    database=self.database
                )

            # Evolve population for next generation
            self.population = self._evolve_population(gen)
            gen += 1

    def _create_initial_population(self) -> list[EvolutionaryPlayer]:
        """Create generation 0 with uniform gene distribution."""
        return [
            self.factory.create_initial_player(generation=0)
            for _ in range(self.config.population_size)
        ]

    def _run_generation_tournament(self):
        """Run FairTournament for current population."""
        # Convert to LLMPlayer instances
        llm_players = [self._to_llm_player(p) for p in self.population]

        # Create tournament config
        tournament_config = BaseTournamentConfig(
            game_description=self.config.game_description,
            repetitions=self.config.repetitions
        )

        # Run tournament
        tournament = FairTournament(llm_players, tournament_config)
        results = tournament.run_tournament()

        # Update fitness in EvolutionaryPlayer instances
        for evo_player, player_id in zip(self.population, results.player_ids):
            stats = results.player_stats[player_id]
            evo_player.fitness = stats.mean_payoff

    def _to_llm_player(self, evo_player: EvolutionaryPlayer) -> LLMPlayer:
        """Convert EvolutionaryPlayer to LLMPlayer for games."""
        return LLMPlayer(
            name=f"player_{evo_player.player_id}",
            attitude=evo_player.gene.attitude,
            game_description=self.config.game_description,
            strategy_class=evo_player.strategy_class
        )

    def _record_snapshot(self, generation: int) -> GenerationSnapshot:
        """Record current generation state."""
        # Count gene frequencies
        gene_freq = {}
        for player in self.population:
            gene_freq[player.gene] = gene_freq.get(player.gene, 0) + 1

        # Count attitude frequencies
        attitude_freq = {}
        for player in self.population:
            att = player.gene.attitude
            attitude_freq[att] = attitude_freq.get(att, 0) + 1

        # Count provider frequencies
        provider_freq = {}
        for player in self.population:
            prov = player.gene.provider_model
            provider_freq[prov] = provider_freq.get(prov, 0) + 1

        # Get fitness stats
        fitnesses = [p.fitness for p in self.population]

        # Get elite IDs (sorted by fitness)
        sorted_pop = sorted(self.population, key=lambda p: p.fitness, reverse=True)
        elite_ids = [p.player_id for p in sorted_pop[:self.config.n_elite]]

        return GenerationSnapshot(
            generation=generation,
            gene_frequencies=gene_freq,
            attitude_frequencies=attitude_freq,
            provider_frequencies=provider_freq,
            mean_fitness=sum(fitnesses) / len(fitnesses),
            max_fitness=max(fitnesses),
            min_fitness=min(fitnesses),
            elite_player_ids=elite_ids
        )

    def _check_stopping(self, gen: int, snapshot: GenerationSnapshot) -> str | None:
        """Check if stopping criteria met. Returns reason if stopping, None otherwise."""
        # Check max generations
        if gen >= self.config.max_generations:
            return "max_generations"

        # Check gene frequency threshold
        max_gene_freq = max(snapshot.gene_frequencies.values()) / self.config.population_size
        if max_gene_freq >= self.config.convergence_threshold:
            return "threshold_reached"

        return None

    def _evolve_population(self, generation: int) -> list[EvolutionaryPlayer]:
        """Create next generation via selection and reproduction."""
        # Sort by fitness
        sorted_pop = sorted(self.population, key=lambda p: p.fitness, reverse=True)

        next_gen = []

        # Elites survive (keep exact strategy)
        for elite in sorted_pop[:self.config.n_elite]:
            successor = self.factory.create_elite_successor(elite, generation + 1)
            next_gen.append(successor)

        # Fill remaining slots via fitness-proportional reproduction
        for _ in range(self.config.population_size - self.config.n_elite):
            parent = self._select_parent_fitness_proportional(sorted_pop)
            offspring = self.factory.create_offspring(
                parent=parent,
                generation=generation + 1,
                available_provider_models=self.available_provider_models
            )
            next_gen.append(offspring)

        return next_gen

    def _select_parent_fitness_proportional(self,
                                           population: list[EvolutionaryPlayer]) -> EvolutionaryPlayer:
        """Select parent proportional to fitness."""
        # Shift fitness to be positive (if needed)
        fitnesses = [p.fitness for p in population]
        min_fitness = min(fitnesses)
        if min_fitness < 0:
            fitnesses = [f - min_fitness + 1 for f in fitnesses]
        else:
            fitnesses = [f + 1 for f in fitnesses]  # Add 1 to avoid zero weights

        # Sample proportional to fitness
        total_fitness = sum(fitnesses)
        probs = [f / total_fitness for f in fitnesses]

        return random.choices(population, weights=probs, k=1)[0]


@dataclass
class EvolutionaryResults:
    """Results from an evolutionary tournament."""
    config: EvolutionaryConfig
    generation_snapshots: list[GenerationSnapshot]
    final_generation: int
    convergence_reason: str
    database: PlayerDatabase

    @property
    def dominant_gene(self) -> Gene:
        """Gene with highest final frequency."""
        final_snapshot = self.generation_snapshots[-1]
        return max(final_snapshot.gene_frequencies,
                  key=final_snapshot.gene_frequencies.get)

    @property
    def dominant_gene_frequency(self) -> float:
        """Frequency of dominant gene at end."""
        final_snapshot = self.generation_snapshots[-1]
        return max(final_snapshot.gene_frequencies.values()) / self.config.population_size

    @property
    def converged(self) -> bool:
        """Whether evolution converged to threshold."""
        return self.convergence_reason == "threshold_reached"
