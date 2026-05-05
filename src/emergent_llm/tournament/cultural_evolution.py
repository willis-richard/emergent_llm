"""Cultural evolution under Fermi pairwise-comparison dynamics."""
import logging
import math
import random
from collections import Counter, defaultdict

import numpy as np

from emergent_llm.common import Attitude, Gene
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.players import StrategySpec
from emergent_llm.tournament.configs import (
    BaseTournamentConfig,
    CulturalEvolutionConfig,
)
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.results import (
    CulturalEvolutionResults,
    CulturalEvolutionSummary,
    collapse_to_base,
)

# Per-generation retention map: (gene, strategy class name) -> count
RetentionMap = dict[tuple[Gene, str], int]


class CulturalEvolution:
    """Cultural evolution under Fermi pairwise-comparison imitation
    (Traulsen, Nowak, Pacheco, 2006), per-gene mutation, and strategy refresh
    on genotype change. Runs natively over all attitudes; reporting collapses
    to the two base attitudes."""

    def __init__(self, config: CulturalEvolutionConfig,
                 strategy_registry: StrategyRegistry):
        self.config = config
        self.registry = strategy_registry
        self.logger = logging.getLogger(__name__)

        self._attitudes_by_base: dict[Attitude, list[Attitude]] = defaultdict(list)
        for attitude in Attitude:
            self._attitudes_by_base[attitude.to_base_attitude()].append(attitude)

        if not self.registry.available_models:
            raise ValueError("Strategy registry is empty")

        for model in self.registry.available_models:
            for attitude in Attitude:
                gene = Gene(model, attitude)
                if gene not in self.registry.available_genes:
                    raise ValueError(f"Missing strategies for {gene}")

        self.reset()

    def reset(self):
        self.generation = 0
        self.gene_frequencies: list[dict[Gene, float]] = []
        self.generation_results: list = []
        self.retention_history: list[RetentionMap] = []
        self._initialise_population()

    def _initialise_population(self):
        """Initialise uniformly across all (model, attitude) genotypes."""
        genes = sorted(self.registry.available_genes, key=str)

        per_gene = math.ceil(self.config.population_size / len(genes))
        self.population: list[StrategySpec] = [
            self.registry.sample_spec(gene)
            for gene in genes for _ in range(per_gene)
        ]
        random.shuffle(self.population)
        self.population = self.population[:self.config.population_size]

        self.logger.info(
            "Initialised %d agents over %d genotypes (%d per genotype before truncation)",
            len(self.population), len(genes), per_gene)

    def run_tournament(self) -> CulturalEvolutionResults:
        self.logger.info(
            "Starting cultural evolution: pop=%d, beta=%g, mu=%g, "
            "n_generations=%d, final_window=%d",
            self.config.population_size, self.config.beta,
            self.config.mutation_rate, self.config.n_generations,
            self.config.final_window)

        for _ in range(self.config.n_generations):
            frequencies = self._calculate_gene_frequencies()
            self.gene_frequencies.append(frequencies)
            self.logger.info("Generation %d: %s", self.generation,
                             self._format_frequencies(frequencies))
            self._run_generation()
            self.generation += 1

        # Record post-final-update frequencies so the history covers the
        # entire trajectory, including the state after the last generation's
        # update.
        final_frequencies = self._calculate_gene_frequencies()
        self.gene_frequencies.append(final_frequencies)
        self.logger.info("Generation %d (final): %s", self.generation,
                         self._format_frequencies(final_frequencies))

        window_mean, window_std = self._compute_window_statistics()

        summary = CulturalEvolutionSummary.from_raw_data(
            self.gene_frequencies, self.generation_results,
            self.retention_history, self.config)

        return CulturalEvolutionResults(
            config=self.config,
            final_window_mean_frequencies=window_mean,
            final_window_std_frequencies=window_std,
            gene_frequency_history=self.gene_frequencies,
            retention_history=self.retention_history,
            summary=summary,
            generation_results=self.generation_results,
        )

    def _compute_window_statistics(
            self) -> tuple[dict[Gene, float], dict[Gene, float]]:
        """Mean and population std of base-attitude-collapsed genotype
        frequencies across the final `final_window` recorded states.
        Reporting (dominant_gene, batch summaries) operates at base-attitude
        granularity; the fine-grained history remains on
        CulturalEvolutionResults.gene_frequency_history."""
        window = [collapse_to_base(g) for g in
                  self.gene_frequencies[-self.config.final_window:]]
        all_genes: set[Gene] = set()
        for gen_freqs in window:
            all_genes.update(gen_freqs.keys())

        means: dict[Gene, float] = {}
        stds: dict[Gene, float] = {}
        for gene in all_genes:
            values = np.array(
                [gen_freqs.get(gene, 0.0) for gen_freqs in window],
                dtype=np.float64)
            means[gene] = float(values.mean())
            stds[gene] = float(values.std(ddof=0))

        means = dict(sorted(means.items(), key=lambda kv: kv[1], reverse=True))
        stds = {g: stds[g] for g in means}
        return means, stds

    def _run_generation(self):
        """Play, then synchronously imitate, mutate, and refresh strategies."""
        # 1. Play
        players = [
            spec.create_player(f"player_{i}", self.config.game_description)
            for i, spec in enumerate(self.population)
        ]
        fair_config = BaseTournamentConfig(
            game_description=self.config.game_description,
            repetitions=self.config.games_per_agent,
            n_processes=1)
        results = FairTournament(players, fair_config).run_tournament()
        self.generation_results.append(results)

        scores_by_name = results.results_df.set_index(
            'player_name')['total_payoff'].to_dict()
        fitnesses = np.array(
            [scores_by_name[p.id.name] for p in players], dtype=np.float64)

        pi_max = self.config.game_description.max_payoff() * self.config.games_per_agent
        pi_min = self.config.game_description.min_payoff() * self.config.games_per_agent
        fitnesses_normalised = (fitnesses - pi_min) / (pi_max - pi_min)

        # 2. Imitation (Fermi pairwise-comparison)
        new_genes, imitated = self._imitate(fitnesses_normalised)

        # 3. Mutation (per-gene independent)
        new_genes, mutated = self._mutate(new_genes)

        # 4. Strategy refresh + retention bookkeeping
        changed = imitated | mutated
        new_population = [
            self.registry.sample_spec(new_genes[i]) if changed[i] else spec
            for i, spec in enumerate(self.population)
        ]
        retention = Counter(
            (spec.gene, spec.strategy_class.__name__)
            for i, spec in enumerate(self.population) if not changed[i])

        self.population = new_population
        self.retention_history.append(retention)

        self.logger.info(
            "Generation %d: imitated=%d, mutated=%d, retained=%d",
            self.generation, int(imitated.sum()), int(mutated.sum()),
            len(self.population) - int(changed.sum()))

    def _imitate(self, fitnesses: np.ndarray) -> tuple[list[Gene], np.ndarray]:
        """Fermi pairwise-comparison rule (Traulsen, Nowak, Pacheco, 2006)."""
        n = len(fitnesses)
        partners = (np.arange(n) + np.random.randint(1, n, size=n)) % n
        deltas = fitnesses[partners] - fitnesses
        probs = 1.0 / (1.0 + np.exp(-self.config.beta * deltas))
        copy_decision = np.random.random(n) < probs

        current_genes = [spec.gene for spec in self.population]
        new_genes: list[Gene] = []
        imitate_mask = np.zeros(n, dtype=bool)
        for i in range(n):
            if copy_decision[i]:
                partner_gene = current_genes[partners[i]]
                new_genes.append(partner_gene)
                if partner_gene != current_genes[i]:
                    imitate_mask[i] = True
            else:
                new_genes.append(current_genes[i])
        return new_genes, imitate_mask

    def _mutate(self, genes: list[Gene]) -> tuple[list[Gene], np.ndarray]:
        """Per-gene independent mutation. Model mutates uniformly to a
        different model. Attitude mutates by flipping its base attitude and
        uniformly sampling one of the four sub-attitudes mapping to the new
        base."""
        mu = self.config.mutation_rate
        models = sorted(self.registry.available_models)

        new_genes = list(genes)
        mutated = np.zeros(len(genes), dtype=bool)

        for i, gene in enumerate(genes):
            new_model = gene.model
            new_attitude = gene.attitude

            if len(models) > 1 and random.random() < mu:
                new_model = random.choice([m for m in models if m != gene.model])
                mutated[i] = True

            if random.random() < mu:
                other_base = gene.attitude.to_base_attitude().flip()
                new_attitude = random.choice(self._attitudes_by_base[other_base])
                mutated[i] = True

            new_genes[i] = Gene(new_model, new_attitude)

        return new_genes, mutated

    def _calculate_gene_frequencies(self) -> dict[Gene, float]:
        """Fine-grained (model, attitude) frequencies for the current
        population."""
        counts = Counter(spec.gene for spec in self.population)
        total = len(self.population)
        return dict(
            sorted(((g, c / total) for g, c in counts.items()),
                   key=lambda kv: kv[1], reverse=True))

    @staticmethod
    def _format_frequencies(frequencies: dict[Gene, float]) -> str:
        """Log base-attitude collapsed frequencies; the full 8-attitude × N-model
        table is too noisy for per-generation logging."""
        collapsed = collapse_to_base(frequencies)
        sorted_items = sorted(collapsed.items(), key=lambda kv: kv[1],
                              reverse=True)
        return ", ".join(f"{g}: {f:.2%}" for g, f in sorted_items)
