"""Tournament results dataclasses."""
import gzip
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator, MultipleLocator

from emergent_llm.common import Attitude, Gene, PlayerId, setup
from emergent_llm.games import get_description_type
from emergent_llm.tournament.configs import (
    BaseTournamentConfig,
    BatchCulturalEvolutionConfig,
    BatchTournamentConfig,
    CulturalEvolutionConfig,
    MixtureKey,
    OutputStyle,
    SurvivorRecord,
)

FIGSIZE, FORMAT = setup('3_col_paper')

MODELS_MAP = {
    "gpt-5-mini[collective]": "GPT 5 Mini[Collective]",
    "gemini-2.5-flash[collective]": "Gemini 2.5 Flash[Collective]",
    "claude-haiku-4-5[collective]": "Claude Haiku 4.5[Collective]",
    "llama3.1-70b[collective]": "Llama 3.1 70b[Collective]",
    "mistral-7b[collective]": "Mistral 7b[Collective]",
    "deepseek-r1-distill-llama-70b[collective]": "DeepSeek R1[Collective]",
    "gpt-5-mini[exploitative]": "GPT 5 Mini[Exploitative]",
    "gemini-2.5-flash[exploitative]": "Gemini 2.5 Flash[Exploitative]",
    "claude-haiku-4-5[exploitative]": "Claude Haiku 4.5[Exploitative]",
    "llama3.1-70b[exploitative]": "Llama 3.1 70b[Exploitative]",
    "mistral-7b[exploitative]": "Mistral 7b[Exploitative]",
    "deepseek-r1-distill-llama-70b[exploitative]": "DeepSeek R1[Exploitative]",
}


def _load_json(filepath: Path) -> dict:
    """Load JSON from gzipped or plain file based on extension."""
    filepath = Path(filepath)
    if filepath.suffix == '.gz':
        with gzip.open(filepath, 'rt', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(filepath, 'r') as f:
            return json.load(f)


def _save_json(filepath: Path, data: dict) -> None:
    """Save JSON to gzipped or plain file based on extension."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    if filepath.suffix == '.gz':
        with gzip.open(filepath, 'wt', encoding='utf-8') as f:
            json.dump(data, f)
    else:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def _find_file(output_dir: Path, filename: str) -> Path:
    """Find a file with either .json or .json.gz extension."""
    for suffix in ['.json.gz', '.json']:
        filepath = output_dir / f"{filename}{suffix}"
        if filepath.exists():
            return filepath
    raise FileNotFoundError(f"No {filename}.json[.gz] found in {output_dir}")


# --- Summary Classes ---


@dataclass(frozen=True)
class FairTournamentSummary:
    """Summary statistics from a fair tournament."""
    results_df: pd.DataFrame

    def to_dict(self) -> dict:
        return {'results': self.results_df.to_dict(orient='records')}

    @classmethod
    def from_dict(cls, data: dict) -> 'FairTournamentSummary':
        return cls(results_df=pd.DataFrame.from_records(data['results']))

    @classmethod
    def from_match_results(
            cls, match_results: list['MatchResult'],
            player_ids: list[PlayerId]) -> 'FairTournamentSummary':
        """Compute summary from raw match data."""
        stats: dict[PlayerId, PlayerStats] = {}
        for mr in match_results:
            for pid, payoff, coops in zip(mr.player_ids, mr.total_payoffs,
                                          mr.total_cooperations):
                if pid not in stats:
                    stats[pid] = PlayerStats(player_id=pid)
                stats[pid].add_game_result(payoff, coops)

        rows = []
        for player_stat in stats.values():
            rows.append({
                'player_name':
                    player_stat.player_id.name,
                'player_attitude':
                    player_stat.player_id.attitude.value
                    if player_stat.player_id.attitude else None,
                'player_strategy':
                    player_stat.player_id.strategy,
                'games_played':
                    player_stat.games_played,
                'mean_payoff':
                    player_stat.mean_payoff,
                'total_payoff':
                    player_stat.total_payoff,
                'total_cooperations':
                    player_stat.total_cooperations,
                'mean_cooperations':
                    player_stat.mean_cooperations,
            })
        results_df = pd.DataFrame(rows).sort_values('mean_payoff',
                                                    ascending=False)
        results_df.sort_index(inplace=True)
        return cls(results_df=results_df)


@dataclass(frozen=True)
class MixtureTournamentSummary:
    """Summary statistics from a mixture tournament."""
    results_df: pd.DataFrame

    def to_dict(self) -> dict:
        return {'results': self.results_df.to_dict(orient='records')}

    @classmethod
    def from_dict(cls, data: dict) -> 'MixtureTournamentSummary':
        return cls(results_df=pd.DataFrame.from_records(data['results']))

    @classmethod
    def from_match_results(
            cls, match_results: list['MatchResult'],
            config: BaseTournamentConfig) -> 'MixtureTournamentSummary':
        """Compute summary from raw match data."""
        mixture_stats: dict[MixtureKey, MixtureResult] = {}

        for match_result in match_results:
            n_collective = sum(1 for pid in match_result.player_ids
                               if pid.attitude == Attitude.COLLECTIVE)
            n_exploitative = sum(1 for pid in match_result.player_ids
                                 if pid.attitude == Attitude.EXPLOITATIVE)

            mixture_key = MixtureKey(n_collective, n_exploitative)
            group_size = n_collective + n_exploitative

            if mixture_key not in mixture_stats:
                mixture_stats[mixture_key] = MixtureResult(
                    group_size=group_size,
                    n_collective=n_collective,
                    n_exploitative=n_exploitative,
                    collective_scores=[],
                    exploitative_scores=[],
                    matches_played=0)

            stats = mixture_stats[mixture_key]
            for player_id, total_payoff in zip(match_result.player_ids,
                                               match_result.total_payoffs):
                if player_id.attitude == Attitude.COLLECTIVE:
                    stats.collective_scores.append(total_payoff)
                elif player_id.attitude == Attitude.EXPLOITATIVE:
                    stats.exploitative_scores.append(total_payoff)
            stats.matches_played += 1

        rows = []
        for result in mixture_stats.values():
            rows.append({
                'group_size': result.group_size,
                'exploitative_ratio': result.exploitative_ratio,
                'collective_ratio': result.collective_ratio,
                'n_collective': result.n_collective,
                'n_exploitative': result.n_exploitative,
                'mean_collective_score': result.mean_collective_score,
                'mean_exploitative_score': result.mean_exploitative_score,
                'mean_social_welfare': result.mean_social_welfare,
                'matches_played': result.matches_played,
            })
        return cls(results_df=pd.DataFrame(rows))


@dataclass(frozen=True)
class CulturalEvolutionSummary:
    """Summary statistics from cultural evolution tournament."""
    gene_frequency_df: pd.DataFrame
    generation_stats_df: pd.DataFrame
    survivor_summary_df: pd.DataFrame

    def to_dict(self) -> dict:
        return {
            'gene_frequency':
                self.gene_frequency_df.to_dict(orient='records'),
            'generation_stats':
                self.generation_stats_df.to_dict(orient='records'),
            'survivor_summary':
                self.survivor_summary_df.to_dict(orient='records'),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CulturalEvolutionSummary':
        gene_freq_df = pd.DataFrame.from_records(data['gene_frequency'])
        gene_freq_df.index.name = 'generation'
        gen_stats_df = pd.DataFrame.from_records(data['generation_stats'])
        gen_stats_df.index.name = 'generation'
        return cls(
            gene_frequency_df=gene_freq_df,
            generation_stats_df=gen_stats_df,
            survivor_summary_df=pd.DataFrame.from_records(
                data['survivor_summary']),
        )

    @classmethod
    def from_raw_data(
            cls, gene_frequency_history: list[dict[Gene, float]],
            survivor_history: list[list[SurvivorRecord]],
            generation_results: list['FairTournamentResults'],
            config: CulturalEvolutionConfig) -> 'CulturalEvolutionSummary':
        """Compute summary from raw data."""
        gene_frequency_df = cls._build_gene_frequency_df(gene_frequency_history)
        generation_stats_df = cls._build_generation_stats_df(
            generation_results, gene_frequency_history, config)
        survivor_summary_df = cls._build_survivor_summary_df(survivor_history)
        return cls(
            gene_frequency_df=gene_frequency_df,
            generation_stats_df=generation_stats_df,
            survivor_summary_df=survivor_summary_df,
        )

    @staticmethod
    def _build_gene_frequency_df(
            gene_frequency_history: list[dict[Gene, float]]) -> pd.DataFrame:
        all_genes = set()
        for gen_freqs in gene_frequency_history:
            all_genes.update(gen_freqs.keys())
        all_genes = sorted(all_genes, key=str)

        rows = []
        for gen_freqs in gene_frequency_history:
            row = {str(gene): gen_freqs.get(gene, 0.0) for gene in all_genes}
            rows.append(row)

        df = pd.DataFrame(rows)
        df.index.name = 'generation'
        return df

    @staticmethod
    def _build_generation_stats_df(
            generation_results: list['FairTournamentResults'],
            gene_frequency_history: list[dict[Gene, float]],
            config: CulturalEvolutionConfig) -> pd.DataFrame:
        stats_rows = []
        total_rounds = config.game_description.n_rounds

        for generation, gen_result in enumerate(generation_results):
            collective_payoffs = []
            exploitative_payoffs = []
            all_payoffs = []
            cooperations = []

            for _, row in gen_result.summary.results_df.iterrows():
                all_payoffs.append(row['mean_payoff'])
                cooperations.append(row['mean_cooperations'] / total_rounds)

                if row['player_attitude'] == Attitude.COLLECTIVE.value:
                    collective_payoffs.append(row['mean_payoff'])
                elif row['player_attitude'] == Attitude.EXPLOITATIVE.value:
                    exploitative_payoffs.append(row['mean_payoff'])

            gen_freqs = gene_frequency_history[generation]
            collective_freq = sum(freq for gene, freq in gen_freqs.items()
                                  if gene.attitude == Attitude.COLLECTIVE)

            stats_rows.append({
                'collective_mean_payoff':
                    np.mean(collective_payoffs)
                    if collective_payoffs else np.nan,
                'exploitative_mean_payoff':
                    np.mean(exploitative_payoffs)
                    if exploitative_payoffs else np.nan,
                'overall_mean_payoff':
                    np.mean(all_payoffs),
                'cooperation_rate':
                    np.mean(cooperations),
                'collective_frequency':
                    collective_freq,
                'exploitative_frequency':
                    1 - collective_freq,
            })

        df = pd.DataFrame(stats_rows)
        df.index.name = 'generation'
        return df

    @staticmethod
    def _build_survivor_summary_df(
            survivor_history: list[list[SurvivorRecord]]) -> pd.DataFrame:
        strategy_counts: Counter[str] = Counter()
        strategy_genes: dict[str, Gene] = {}
        strategy_total_fitness: dict[str, float] = Counter()

        for gen_survivors in survivor_history:
            for record in gen_survivors:
                strategy_counts[record.name] += 1
                strategy_genes[record.name] = record.gene
                strategy_total_fitness[record.name] += record.fitness

        rows = []
        for name, count in strategy_counts.most_common():
            gene = strategy_genes[name]
            avg_fitness = strategy_total_fitness[name] / count
            rows.append({
                'strategy':
                    name,
                'gene':
                    str(gene),
                'model':
                    gene.model,
                'attitude':
                    gene.attitude.value,
                'survival_count':
                    count,
                'survival_rate':
                    count / len(survivor_history) if survivor_history else 0,
                'mean_fitness':
                    avg_fitness,
            })

        return pd.DataFrame(rows)


# --- Helper Classes ---


@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    player_ids: list[PlayerId]
    total_payoffs: list[float]
    total_cooperations: list[int]

    def serialise(self, player_id_to_index: dict[PlayerId, int]) -> dict:
        return {
            'match_id': self.match_id,
            'player_indices': [
                player_id_to_index[pid] for pid in self.player_ids
            ],
            'total_payoffs': self.total_payoffs,
            'total_cooperations': self.total_cooperations,
        }

    @classmethod
    def from_dict(cls, data: dict,
                  index_to_player_id: list[PlayerId]) -> 'MatchResult':
        return cls(
            match_id=data['match_id'],
            player_ids=[index_to_player_id[i] for i in data['player_indices']],
            total_payoffs=data['total_payoffs'],
            total_cooperations=data['total_cooperations'])


@dataclass
class PlayerStats:
    """Statistics for a single player across all games."""
    player_id: PlayerId
    payoffs: list[float] = field(default_factory=list)
    cooperations: list[int] = field(default_factory=list)

    @property
    def games_played(self) -> int:
        return len(self.payoffs)

    @property
    def mean_payoff(self) -> float:
        return float(np.mean(self.payoffs)) if self.payoffs else 0.0

    @property
    def total_payoff(self) -> float:
        return sum(self.payoffs)

    @property
    def mean_cooperations(self) -> float:
        return float(np.mean(self.cooperations)) if self.cooperations else 0.0

    @property
    def total_cooperations(self) -> int:
        return sum(self.cooperations)

    def add_game_result(self, payoff: float, cooperations: int) -> None:
        self.payoffs.append(payoff)
        self.cooperations.append(cooperations)


@dataclass
class MixtureResult:
    """Results for a specific mixture configuration."""
    group_size: int
    n_collective: int
    n_exploitative: int
    collective_scores: list[float]
    exploitative_scores: list[float]
    matches_played: int

    def __post_init__(self):
        if not (self.n_collective + self.n_exploitative == self.group_size):
            raise ValueError(
                f"n_collective ({self.n_collective}) + n_exploitative ({self.n_exploitative}) "
                f"must equal group_size ({self.group_size})")

    @property
    def exploitative_ratio(self) -> float:
        return self.n_exploitative / self.group_size

    @property
    def collective_ratio(self) -> float:
        return self.n_collective / self.group_size

    @property
    def mean_collective_score(self) -> float:
        return float(np.mean(
            self.collective_scores)) if self.collective_scores else np.nan

    @property
    def mean_exploitative_score(self) -> float:
        return float(np.mean(
            self.exploitative_scores)) if self.exploitative_scores else np.nan

    @property
    def mean_social_welfare(self) -> float:
        all_scores = self.collective_scores + self.exploitative_scores
        return float(np.mean(all_scores)) if all_scores else np.nan


# --- Results Classes ---


@dataclass(frozen=True)
class FairTournamentResults:
    """Results from a fair tournament."""
    FILENAME = "fair_tournament"

    config: BaseTournamentConfig
    player_ids: list[PlayerId]
    summary: FairTournamentSummary
    match_results: list[MatchResult] | None = None

    def __post_init__(self):
        if self.match_results is not None:
            games_played = self.summary.results_df['games_played'].unique()
            if len(games_played) > 1:
                raise ValueError(f"Inconsistent games played: {games_played}")

    @property
    def results_df(self) -> pd.DataFrame:
        return self.summary.results_df

    def __str__(self) -> str:
        df = self.summary.results_df
        type_summary = df.groupby('player_attitude')['total_payoff'].agg(
            ['mean', 'std', 'count'])
        output = str(type_summary)
        output += f"\n\nTotal players: {len(df)}"
        if self.match_results:
            output += f"\nTotal matches: {len(self.match_results)}"
        else:
            output += "\n(Loaded from summary — match details unavailable)"
        return output

    def serialise(self, style: OutputStyle = OutputStyle.FULL) -> dict:
        data = {
            'config': self.config.serialise(),
            'player_ids': [asdict(pid) for pid in self.player_ids],
            'result_type': 'FairTournamentResults',
        }

        if style == OutputStyle.SUMMARY or self.match_results is None:
            data['summary'] = self.summary.to_dict()
        else:
            player_id_to_index = {
                pid: i for i, pid in enumerate(self.player_ids)
            }
            data['match_results'] = [
                mr.serialise(player_id_to_index) for mr in self.match_results
            ]

        return data

    def save(self,
             output_dir: Path,
             style: OutputStyle = OutputStyle.FULL) -> Path:
        output_dir = Path(output_dir)
        filepath = output_dir / f"{self.FILENAME}{style.get_suffix()}"
        _save_json(filepath, self.serialise(style))
        return filepath

    @classmethod
    def from_dict(cls, data: dict) -> 'FairTournamentResults':
        config = BaseTournamentConfig.from_dict(data['config'])
        player_ids = [
            PlayerId.from_dict(pid_data) for pid_data in data['player_ids']
        ]

        if 'match_results' in data:
            match_results = [
                MatchResult.from_dict(mr, player_ids)
                for mr in data['match_results']
            ]
            summary = FairTournamentSummary.from_match_results(
                match_results, player_ids)
        else:
            match_results = None
            summary = FairTournamentSummary.from_dict(data['summary'])

        return cls(config=config,
                   player_ids=player_ids,
                   summary=summary,
                   match_results=match_results)

    @classmethod
    def load(cls, output_dir: Path) -> 'FairTournamentResults':
        filepath = _find_file(Path(output_dir), cls.FILENAME)
        data = _load_json(filepath)
        if data.get('result_type') != 'FairTournamentResults':
            raise ValueError(
                f"Expected FairTournamentResults, got {data.get('result_type')}"
            )
        return cls.from_dict(data)


@dataclass(frozen=True)
class MixtureTournamentResults:
    """Results from a mixture tournament."""
    FILENAME = "mixture_tournament"

    config: BaseTournamentConfig
    collective_player_ids: list[PlayerId]
    exploitative_player_ids: list[PlayerId]
    summary: MixtureTournamentSummary
    match_results: list[MatchResult] | None = None

    @property
    def results_df(self) -> pd.DataFrame:
        return self.summary.results_df

    def __str__(self) -> str:
        return str(self.summary.results_df)

    def serialise(self, style: OutputStyle = OutputStyle.FULL) -> dict:
        data = {
            'config': self.config.serialise(),
            'collective_player_ids': [
                asdict(pid) for pid in self.collective_player_ids
            ],
            'exploitative_player_ids': [
                asdict(pid) for pid in self.exploitative_player_ids
            ],
            'result_type': 'MixtureTournamentResults',
        }

        if style == OutputStyle.SUMMARY or self.match_results is None:
            data['summary'] = self.summary.to_dict()
        else:
            all_players = self.collective_player_ids + self.exploitative_player_ids
            player_id_to_index = {pid: i for i, pid in enumerate(all_players)}
            data['match_results'] = [
                mr.serialise(player_id_to_index) for mr in self.match_results
            ]

        return data

    def save(self,
             output_dir: Path,
             style: OutputStyle = OutputStyle.FULL) -> Path:
        output_dir = Path(output_dir)
        filepath = output_dir / f"{self.FILENAME}{style.get_suffix()}"
        _save_json(filepath, self.serialise(style))
        return filepath

    @classmethod
    def from_dict(cls, data: dict) -> 'MixtureTournamentResults':
        config = BaseTournamentConfig.from_dict(data['config'])
        collective_ids = [
            PlayerId.from_dict(d) for d in data['collective_player_ids']
        ]
        exploitative_ids = [
            PlayerId.from_dict(d) for d in data['exploitative_player_ids']
        ]

        if 'match_results' in data:
            all_players = collective_ids + exploitative_ids
            match_results = [
                MatchResult.from_dict(mr, all_players)
                for mr in data['match_results']
            ]
            summary = MixtureTournamentSummary.from_match_results(
                match_results, config)
        else:
            match_results = None
            summary = MixtureTournamentSummary.from_dict(data['summary'])

        return cls(config=config,
                   collective_player_ids=collective_ids,
                   exploitative_player_ids=exploitative_ids,
                   summary=summary,
                   match_results=match_results)

    @classmethod
    def load(cls, output_dir: Path) -> 'MixtureTournamentResults':
        filepath = _find_file(Path(output_dir), cls.FILENAME)
        data = _load_json(filepath)
        if data.get('result_type') != 'MixtureTournamentResults':
            raise ValueError(
                f"Expected MixtureTournamentResults, got {data.get('result_type')}"
            )
        return cls.from_dict(data)

    def create_schelling_diagram(self, output_dir: str):
        sorted_results = self.summary.results_df.sort_values('n_collective')

        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        n_collective = sorted_results['n_collective'].values
        collective_scores = sorted_results[
            'mean_collective_score'].values / self.config.game_description.n_rounds
        exploitative_scores = sorted_results[
            'mean_exploitative_score'].values / self.config.game_description.n_rounds

        collective_scores = np.roll(collective_scores, -1)

        ax.plot(n_collective,
                collective_scores,
                label='Collective',
                lw=0.75,
                marker='o',
                clip_on=False)
        ax.plot(n_collective,
                exploitative_scores,
                label='Exploitative',
                lw=0.75,
                marker='s',
                clip_on=False)

        gd = self.config.game_description
        ax.set_xlabel('Number of collective co-players')
        ax.set_ylabel('Normalised reward')
        ax.set_xlim(0, gd.n_players - 1)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))
        ax.set_ylim(math.floor(gd.normalised_min_payoff()),
                    math.ceil(gd.normalised_max_payoff()))
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.axhline(y=gd.normalised_min_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')
        plt.axhline(y=gd.normalised_max_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')
        plt.axhline(y=gd.normalised_max_payoff(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')

        ax.legend(bbox_to_anchor=(0, 1.4),
                  loc='upper left',
                  ncol=2,
                  frameon=False,
                  columnspacing=0.5)

        output_file = Path(output_dir) / f"schelling_n_{gd.n_players}.{FORMAT}"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)


@dataclass
class CulturalEvolutionResults:
    """Results from cultural evolution tournament."""
    FILENAME = "cultural_evolution"

    config: CulturalEvolutionConfig
    final_generation: int
    final_gene_frequencies: dict[Gene, float]
    gene_frequency_history: list[dict[Gene, float]]
    survivor_history: list[list[SurvivorRecord]]
    summary: CulturalEvolutionSummary
    generation_results: list[FairTournamentResults] | None = None

    @property
    def gene_frequency_df(self) -> pd.DataFrame:
        return self.summary.gene_frequency_df

    @property
    def generation_stats_df(self) -> pd.DataFrame:
        return self.summary.generation_stats_df

    @property
    def survivor_summary_df(self) -> pd.DataFrame:
        return self.summary.survivor_summary_df

    @property
    def winning_gene(self) -> Gene:
        return max(self.final_gene_frequencies.items(), key=lambda x: x[1])[0]

    def __str__(self) -> str:
        lines = [
            f"Cultural Evolution Results",
            f"Final generation: {self.final_generation}",
            f"Final gene frequencies:"
        ]
        for gene, freq in sorted(self.final_gene_frequencies.items(),
                                 key=lambda x: x[1],
                                 reverse=True):
            lines.append(f"  {gene}: {freq:.2%}")

        lines.append(
            f"\nTop surviving strategies (across {len(self.survivor_history)} generations):"
        )
        for _, row in self.survivor_summary_df.head(10).iterrows():
            lines.append(
                f"  {row['strategy']} ({row['gene']}): "
                f"survived {row['survival_count']}x, mean fitness {row['mean_fitness']:.2f}"
            )

        return "\n".join(lines)

    def serialise(self, style: OutputStyle = OutputStyle.FULL) -> dict:
        config_dict = asdict(self.config)
        config_dict['game_description'][
            '__class__'] = self.config.game_description.__class__.__name__

        data = {
            'config': config_dict,
            'final_generation': self.final_generation,
            'final_gene_frequencies': [{
                'gene': asdict(gene),
                'frequency': freq
            } for gene, freq in self.final_gene_frequencies.items()],
            'gene_frequency_history':
                [[{
                    'gene': asdict(gene),
                    'frequency': freq
                }
                  for gene, freq in gen_freqs.items()]
                 for gen_freqs in self.gene_frequency_history],
            'survivor_history': [[record.to_dict()
                                  for record in gen_survivors]
                                 for gen_survivors in self.survivor_history],
            'result_type': 'CulturalEvolutionResults',
        }

        if style == OutputStyle.SUMMARY or self.generation_results is None:
            data['generation_stats'] = self.summary.generation_stats_df.to_dict(
                orient='records')
        else:
            data['generation_results'] = [
                r.serialise(style) for r in self.generation_results
            ]

        return data

    def save(self,
             output_dir: Path,
             style: OutputStyle = OutputStyle.FULL) -> Path:
        output_dir = Path(output_dir)
        filepath = output_dir / f"{self.FILENAME}{style.get_suffix()}"
        _save_json(filepath, self.serialise(style))
        return filepath

    @classmethod
    def from_dict(cls, data: dict) -> 'CulturalEvolutionResults':
        config_data = data['config']
        game_cls = get_description_type(
            config_data['game_description']['__class__'])
        game_description = game_cls(
            **{
                k: v
                for k, v in config_data['game_description'].items()
                if k != '__class__'
            })

        config = CulturalEvolutionConfig(
            game_description=game_description,
            population_size=config_data['population_size'],
            top_k=config_data['top_k'],
            mutation_rate=config_data['mutation_rate'],
            threshold_pct=config_data['threshold_pct'],
            max_generations=config_data['max_generations'],
            repetitions_per_generation=config_data['repetitions_per_generation']
        )

        final_gene_frequencies = {
            Gene.from_dict(item['gene']): item['frequency']
            for item in data['final_gene_frequencies']
        }

        gene_frequency_history = [{
            Gene.from_dict(item['gene']): item['frequency'] for item in gen_freqs
        } for gen_freqs in data['gene_frequency_history']]

        survivor_history = [[
            SurvivorRecord.from_dict(record) for record in gen_survivors
        ] for gen_survivors in data['survivor_history']]

        if 'generation_results' in data:
            generation_results = [
                FairTournamentResults.from_dict(r)
                for r in data['generation_results']
            ]
            summary = CulturalEvolutionSummary.from_raw_data(
                gene_frequency_history, survivor_history, generation_results,
                config)
        else:
            generation_results = None
            gene_frequency_df = CulturalEvolutionSummary._build_gene_frequency_df(
                gene_frequency_history)
            survivor_summary_df = CulturalEvolutionSummary._build_survivor_summary_df(
                survivor_history)
            generation_stats_df = pd.DataFrame.from_records(
                data['generation_stats'])
            generation_stats_df.index.name = 'generation'
            summary = CulturalEvolutionSummary(
                gene_frequency_df=gene_frequency_df,
                generation_stats_df=generation_stats_df,
                survivor_summary_df=survivor_summary_df)

        return cls(config=config,
                   final_generation=data['final_generation'],
                   final_gene_frequencies=final_gene_frequencies,
                   gene_frequency_history=gene_frequency_history,
                   survivor_history=survivor_history,
                   summary=summary,
                   generation_results=generation_results)

    @classmethod
    def load(cls, output_dir: Path) -> 'CulturalEvolutionResults':
        filepath = _find_file(Path(output_dir), cls.FILENAME)
        data = _load_json(filepath)
        if data.get('result_type') != 'CulturalEvolutionResults':
            raise ValueError(
                f"Expected CulturalEvolutionResults, got {data.get('result_type')}"
            )
        return cls.from_dict(data)

    def plot_gene_frequencies(self, output_dir: Path):
        # increase space for legend

        figsize, _ = setup('1_col_slide')

        cmap = plt.cm.Paired
        colors = [cmap(i) for i in np.linspace(0, 1, len(self.gene_frequency_df.columns))]

        # increase room for legend
        fig, ax = plt.subplots(figsize=(FIGSIZE[0], FIGSIZE[1] * 2.1),
                               facecolor='white')

        for i, col in enumerate(self.gene_frequency_df.columns):
            ax.plot(self.gene_frequency_df.index,
                    self.gene_frequency_df[col],
                    marker='o',
                    lw=0.75,
                    label=MODELS_MAP[col],
                    color=colors[i],
                    clip_on=False)

        ax.set_xlabel('Generation')
        ax.set_ylabel('Gene Frequency')
        ax.set_ylim(0, 1)
        ax.legend(bbox_to_anchor=(1, -0.5), loc='lower left', frameon=False,
                  ncols=1, handletextpad=0.4, columnspacing=0.6)
        ax.grid(True, alpha=0.3)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"gene_frequencies.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plot_attitude_evolution(self, output_dir: Path):
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['collective_frequency'],
                label='Collective',
                marker='o',
                lw=0.75,
                clip_on=False)
        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['exploitative_frequency'],
                label='Exploitative',
                marker='s',
                lw=0.75,
                clip_on=False)

        ax.set_xlabel('Generation')
        ax.set_ylabel('Proportion')
        ax.set_ylim(0, 1)
        ax.legend(bbox_to_anchor=(0, 1.4),
                  loc='upper left',
                  ncol=2,
                  frameon=False,
                  columnspacing=0.5)
        ax.grid(True, alpha=0.3)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"attitude_evolution.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plot_cooperation_evolution(self, output_dir: Path):
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['cooperation_rate'],
                marker='o',
                lw=0.75,
                color='green',
                clip_on=False)

        ax.set_xlabel('Generation')
        ax.set_ylabel('Cooperation Rate')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"cooperation_evolution.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plot_mean_payoffs(self, output_dir: Path):
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        gd = self.config.game_description
        n_rounds = gd.n_rounds

        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['collective_mean_payoff'] / n_rounds,
                label='Collective',
                marker='o',
                lw=0.75,
                clip_on=False)
        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['exploitative_mean_payoff'] / n_rounds,
                label='Exploitative',
                marker='s',
                lw=0.75,
                clip_on=False)
        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['overall_mean_payoff'] / n_rounds,
                label='Overall',
                marker='^',
                lw=0.75,
                linestyle='--',
                clip_on=False)

        ax.axhline(y=gd.normalised_min_social_welfare(),
                   color='grey',
                   alpha=0.3,
                   linestyle='-')
        ax.axhline(y=gd.normalised_max_social_welfare(),
                   color='grey',
                   alpha=0.3,
                   linestyle='-')
        ax.axhline(y=gd.normalised_max_payoff(),
                   color='grey',
                   alpha=0.3,
                   linestyle='-')

        ax.set_ylim(math.floor(gd.normalised_min_payoff()),
                    math.ceil(gd.normalised_max_payoff() / 10 + 1) * 10)
        ax.yaxis.set_major_locator(MultipleLocator(1))

        ax.set_xlabel('Generation')
        ax.set_ylabel('Mean Payoff')
        ax.legend(bbox_to_anchor=(0, 1.4),
                  loc='upper left',
                  ncol=3,
                  frameon=False,
                  columnspacing=0.5)
        ax.grid(True, alpha=0.3)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"mean_payoffs.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plots(self, output_dir: str | Path):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        self.plot_gene_frequencies(output_dir)
        self.plot_attitude_evolution(output_dir)
        self.plot_cooperation_evolution(output_dir)
        self.plot_mean_payoffs(output_dir)


# --- Batch Results Classes ---


@dataclass(frozen=True)
class BatchFairTournamentResults:
    """Results from a batch fair tournament across multiple group sizes."""
    FILENAME = "batch_fair"

    config: BatchTournamentConfig
    fair_results: dict[int, FairTournamentResults]
    _combined_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if not self.fair_results:
            raise ValueError(
                "Cannot create results with no fair tournament results")

        combined_rows = []
        for group_size, fair_result in self.fair_results.items():
            df = fair_result.summary.results_df.copy()
            df['group_size'] = group_size
            combined_rows.append(df)

        combined_df = pd.concat(combined_rows, ignore_index=True)
        object.__setattr__(self, '_combined_df', combined_df)

    @property
    def combined_df(self) -> pd.DataFrame:
        return self._combined_df

    def __str__(self) -> str:
        lines = [
            f"Batch Fair Tournament Results",
            f"Group sizes: {sorted(self.fair_results.keys())}",
            f"Repetitions per group: {self.config.repetitions}",
        ]

        if 'player_attitude' in self.combined_df.columns:
            summary = self.combined_df.groupby([
                'group_size', 'player_attitude'
            ])['mean_payoff'].agg(['mean', 'std', 'count'])
            lines.extend(
                ["\nPerformance by group size and attitude:",
                 str(summary)])

        return "\n".join(lines)

    def serialise(self) -> dict:
        return {
            'config': asdict(self.config),
            'fair_results': {
                str(gs): result.serialise(self.config.output_style)
                for gs, result in self.fair_results.items()
            },
            'result_type': 'BatchFairTournamentResults'
        }

    def save(self) -> Path:
        filepath = self.config.output_dir / f"{self.FILENAME}{self.config.output_style.get_suffix()}"
        _save_json(filepath, self.serialise())
        return filepath

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchFairTournamentResults':
        config = BatchTournamentConfig(**data['config'])
        fair_results = {
            int(gs): FairTournamentResults.from_dict(rd)
            for gs, rd in data['fair_results'].items()
        }
        return cls(config=config, fair_results=fair_results)

    @classmethod
    def load(cls, output_dir: Path) -> 'BatchFairTournamentResults':
        filepath = _find_file(Path(output_dir), cls.FILENAME)
        data = _load_json(filepath)
        if data.get('result_type') != 'BatchFairTournamentResults':
            raise ValueError(
                f"Expected BatchFairTournamentResults, got {data.get('result_type')}"
            )
        return cls.from_dict(data)


@dataclass(frozen=True)
class BatchMixtureTournamentResults:
    """Results from a batch mixture tournament across multiple group sizes."""
    FILENAME = "batch_mixture"

    config: BatchTournamentConfig
    mixture_results: dict[int, MixtureTournamentResults]
    _combined_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _summary_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if not self.mixture_results:
            raise ValueError(
                "Cannot create results with no mixture tournament results")

        combined_rows = []
        for group_size, result in self.mixture_results.items():
            df = result.summary.results_df.copy()
            df['group_size'] = group_size
            combined_rows.append(df)

        combined_df = pd.concat(combined_rows, ignore_index=True)
        object.__setattr__(self, '_combined_df', combined_df)

        summary_df = combined_df.pivot_table(values='mean_social_welfare',
                                             index='collective_ratio',
                                             columns='group_size',
                                             fill_value=np.nan)
        summary_df.index = [f"{ratio:.0%}" for ratio in summary_df.index]
        object.__setattr__(self, '_summary_df', summary_df)

    @property
    def combined_df(self) -> pd.DataFrame:
        return self._combined_df

    @property
    def summary_df(self) -> pd.DataFrame:
        return self._summary_df

    def __str__(self) -> str:
        pivot_df = self.combined_df.pivot_table(values='mean_social_welfare',
                                                index='collective_ratio',
                                                columns='group_size',
                                                fill_value=np.nan)
        pivot_df.index = [f"{ratio:.0%}" for ratio in pivot_df.index]

        output = "=== SOCIAL WELFARE SUMMARY TABLE ==="
        output += "\nRows: Exploitative player ratio, Columns: Group size"
        output += pivot_df.to_string(float_format='%.3f')
        return output

    def serialise(self) -> dict:
        return {
            'config': asdict(self.config),
            'mixture_results': {
                str(gs): result.serialise(self.config.output_style)
                for gs, result in self.mixture_results.items()
            },
            'result_type': 'BatchMixtureTournamentResults'
        }

    def save(self) -> Path:
        filepath = self.config.output_dir / f"{self.FILENAME}{self.config.output_style.get_suffix()}"
        _save_json(filepath, self.serialise())
        return filepath

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchMixtureTournamentResults':
        config = BatchTournamentConfig(**data['config'])
        mixture_results = {
            int(gs): MixtureTournamentResults.from_dict(rd)
            for gs, rd in data['mixture_results'].items()
        }
        return cls(config=config, mixture_results=mixture_results)

    @classmethod
    def load(cls, output_dir: Path) -> 'BatchMixtureTournamentResults':
        filepath = _find_file(Path(output_dir), cls.FILENAME)
        data = _load_json(filepath)
        if data.get('result_type') != 'BatchMixtureTournamentResults':
            raise ValueError(
                f"Expected BatchMixtureTournamentResults, got {data.get('result_type')}"
            )
        return cls.from_dict(data)

    def create_schelling_diagrams(self):
        for group_size, mixture_result in self.mixture_results.items():
            mixture_result.create_schelling_diagram(self.config.output_dir)

    def create_social_welfare_diagram(self):
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        group_sizes = sorted(self.mixture_results.keys())
        gd = self.mixture_results[group_sizes[-1]].config.game_description

        for group_size in group_sizes:
            group_data = self.combined_df[self.combined_df['group_size'] ==
                                          group_size]
            group_data = group_data.sort_values('collective_ratio')

            ax.plot(group_data['collective_ratio'] * 100,
                    group_data['mean_social_welfare'] / gd.n_rounds,
                    label=f'n={group_size}',
                    lw=1.5,
                    marker='o')

        ax.set_xlabel('Proportion of collective prompts (%)')
        ax.set_ylabel('Normalised reward')
        ax.set_xlim(0, 100)
        ax.set_ylim(math.floor(gd.normalised_min_payoff()),
                    math.ceil(gd.normalised_max_social_welfare()))
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.axhline(y=gd.normalised_min_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')
        plt.axhline(y=gd.normalised_max_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')

        ax.legend(bbox_to_anchor=(-0.13, 1.4),
                  loc='upper left',
                  ncol=len(group_sizes),
                  frameon=False,
                  handletextpad=0.4,
                  columnspacing=0.6)

        output_file = self.config.output_dir / f"social_welfare.{FORMAT}"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def create_relative_schelling_diagram(self):
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        group_sizes = sorted(self.mixture_results.keys())
        gd = self.mixture_results[group_sizes[-1]].config.game_description

        for group_size in group_sizes:
            group_data = self.combined_df[self.combined_df['group_size'] ==
                                          group_size]
            group_data = group_data.sort_values('collective_ratio')

            collective_scores = group_data['mean_collective_score'].values
            rolled_collective_scores = np.roll(collective_scores, -1)[:-1]
            exploitative_scores = group_data[
                'mean_exploitative_score'].values[:-1]
            difference = exploitative_scores - rolled_collective_scores
            normalised_difference = difference / gd.n_rounds

            n_collective = group_data['n_collective'].values
            rolled_n_collective = np.roll(n_collective, -1)[:-1] - 1
            n_exploitative = group_data['n_exploitative'].values[:-1] - 1
            opponent_proportion = rolled_n_collective / (rolled_n_collective +
                                                         n_exploitative)

            ax.plot(opponent_proportion * 100,
                    normalised_difference,
                    label=f'n={group_size}',
                    lw=1.5,
                    marker='o')

        ax.set_xlabel('Opponent collective prompts (%)')
        ax.set_ylabel('Normalised advantage')
        ax.set_xlim(0, 100)
        ax.set_ylim(
            math.floor(gd.normalised_min_payoff() - gd.normalised_max_payoff()),
            math.ceil(gd.normalised_max_payoff() - gd.normalised_min_payoff()))
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.axhline(y=0, color='grey', alpha=0.3, linestyle='-')

        ax.legend(bbox_to_anchor=(-0.13, 1.4),
                  loc='upper left',
                  ncol=len(group_sizes),
                  frameon=False,
                  handletextpad=0.4,
                  columnspacing=0.6)

        output_file = self.config.output_dir / f"schelling_difference.{FORMAT}"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)


@dataclass
class BatchCulturalEvolutionResults:
    """Results from batch cultural evolution tournament."""
    FILENAME = "batch_cultural_evolution"

    config: BatchCulturalEvolutionConfig
    runs: list[CulturalEvolutionResults]
    _run_summary_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _gene_summary_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _strategy_summary_df: pd.DataFrame = field(default=None,
                                               init=False,
                                               repr=False)

    def __post_init__(self):
        if not self.runs:
            raise ValueError("Cannot create results with no runs")

        run_rows = []
        for run_idx, run in enumerate(self.runs):
            winning_gene = run.winning_gene
            winning_frequency = run.final_gene_frequencies[winning_gene]

            n_rounds = run.config.game_description.n_rounds
            normalised_collective_payoff = run.generation_stats_df.iloc[-1]['collective_mean_payoff'] / n_rounds
            normalised_exploitative_payoff = run.generation_stats_df.iloc[-1]['exploitative_mean_payoff'] / n_rounds
            normalised_social_welfare = run.generation_stats_df.iloc[-1]['overall_mean_payoff'] / n_rounds

            run_rows.append({
                'run': run_idx,
                'generations': run.final_generation,
                'winning_gene': str(winning_gene),
                'winning_model': winning_gene.model,
                'winning_attitude': winning_gene.attitude.value,
                'winning_frequency': winning_frequency,
                'threshold_met': winning_frequency >= run.config.threshold_pct,
                'normalised_collective_payoff': normalised_collective_payoff,
                'normalised_exploitative_payoff': normalised_exploitative_payoff,
                'normalised_social_welfare': normalised_social_welfare})

        object.__setattr__(self, '_run_summary_df', pd.DataFrame(run_rows))

        all_genes = set()
        for run in self.runs:
            all_genes.update(run.final_gene_frequencies.keys())

        win_counts = {}
        for run in self.runs:
            winner = run.winning_gene
            win_counts[winner] = win_counts.get(winner, 0) + 1

        gene_rows = []
        for gene in sorted(all_genes, key=str):
            frequencies = [
                run.final_gene_frequencies.get(gene, 0.0)
                for run in self.runs
                if gene in run.final_gene_frequencies
            ]
            wins = win_counts.get(gene, 0)
            gene_rows.append({
                'gene': str(gene),
                'model': gene.model,
                'attitude': gene.attitude.value,
                'wins': wins,
                'win_proportion': wins / len(self.runs),
                'mean_frequency': np.mean(frequencies) if frequencies else 0.0,
                'std_frequency': np.std(frequencies) if frequencies else 0.0,
            })

        object.__setattr__(
            self, '_gene_summary_df',
            pd.DataFrame(gene_rows).sort_values('wins', ascending=False))

        strategy_counts: Counter[str] = Counter()
        strategy_genes: dict[str, Gene] = {}
        strategy_fitness_sum: dict[str, float] = Counter()
        strategy_fitness_count: dict[str, int] = Counter()

        for run in self.runs:
            if run.survivor_history:
                for record in run.survivor_history[-1]:
                    strategy_counts[record.name] += 1
                    strategy_genes[record.name] = record.gene
                    strategy_fitness_sum[record.name] += record.fitness
                    strategy_fitness_count[record.name] += 1

        strat_rows = []
        for name, count in strategy_counts.most_common():
            gene = strategy_genes[name]
            avg_fitness = strategy_fitness_sum[name] / strategy_fitness_count[
                name]
            strat_rows.append({
                'strategy': name,
                'gene': str(gene),
                'model': gene.model,
                'attitude': gene.attitude.value,
                'total_survivals': count,
                'mean_fitness': avg_fitness,
            })

        object.__setattr__(self, '_strategy_summary_df',
                           pd.DataFrame(strat_rows))

    @property
    def run_summary_df(self) -> pd.DataFrame:
        return self._run_summary_df

    @property
    def gene_summary_df(self) -> pd.DataFrame:
        return self._gene_summary_df

    @property
    def strategy_summary_df(self) -> pd.DataFrame:
        return self._strategy_summary_df

    def __str__(self) -> str:
        threshold_met = self.run_summary_df['threshold_met'].sum()
        avg_gens = self.run_summary_df['generations'].mean()

        lines = [
            f"Multi-run cultural evolution: {len(self.runs)} runs",
            f"Threshold reached: {threshold_met}/{len(self.runs)} ({threshold_met/len(self.runs):.1%})",
            f"Average generations: {avg_gens:.1f}",
            "",
            "Gene performance:",
        ]

        display_df = self.gene_summary_df[[
            'gene', 'wins', 'win_proportion', 'mean_frequency', 'std_frequency'
        ]].copy()
        display_df['win_proportion'] = display_df['win_proportion'].apply(
            lambda x: f"{x:.1%}")
        display_df['mean_frequency'] = display_df['mean_frequency'].apply(
            lambda x: f"{x:.3f}")
        display_df['std_frequency'] = display_df['std_frequency'].apply(
            lambda x: f"{x:.3f}")
        display_df.columns = ['Gene', 'Wins', 'Win%', 'Mean', 'Std']
        lines.append(display_df.to_string(index=False))

        lines.append("")
        lines.append("By attitude:")
        for attitude, count in self.run_summary_df[
                'winning_attitude'].value_counts().items():
            lines.append(f"  {attitude}: {count} ({count/len(self.runs):.1%})")

        lines.append("")
        lines.append("By model:")
        for model, count in self.run_summary_df['winning_model'].value_counts(
        ).items():
            lines.append(f"  {model}: {count} ({count/len(self.runs):.1%})")

        lines.append("")
        lines.append("Top surviving strategies (across all runs):")
        for _, row in self._strategy_summary_df.nlargest(
                10, 'total_survivals').iterrows():
            lines.append(
                f"  {row['strategy']} ({row['attitude']}): "
                f"{row['total_survivals']} survivals, fitness={row['mean_fitness']:.2f}"
            )

        n_rounds = self.config.evolution_config.game_description.n_rounds
        social_welfare = self.run_summary_df.normalised_social_welfare.mean()
        max_social_welfare = self.config.evolution_config.game_description.max_social_welfare() / n_rounds
        min_social_welfare = self.config.evolution_config.game_description.min_social_welfare() / n_rounds
        proportion = (social_welfare - min_social_welfare) / (max_social_welfare - min_social_welfare)
        lines.append(f"Normalised collective payoff: {self.run_summary_df.normalised_collective_payoff.mean():.2f}")
        lines.append(f"Normalised exploitative payoff: {self.run_summary_df.normalised_exploitative_payoff.mean():.2f}")
        lines.append(f"Normalised social welfare: {social_welfare:.2f}")
        lines.append(f"Maximum social welfare: {max_social_welfare:.2f}")
        lines.append(f"Minimum social welfare: {min_social_welfare:.2f}")
        lines.append(f"Proportion: {proportion:.2f}")

        return "\n".join(lines)

    def plots(self, output_dir: Path | None = None):
        savepath = self.config.output_dir if output_dir is None else Path(
            output_dir)
        savepath.mkdir(parents=True, exist_ok=True)

        individual_dir = savepath / "individual_runs"
        individual_dir.mkdir(exist_ok=True)
        for idx, run in enumerate(self.runs):
            run.plots(individual_dir / f"run_{idx:03d}")

    def serialise(self) -> dict:
        return {
            'config': asdict(self.config),
            'runs': [
                run.serialise(self.config.output_style) for run in self.runs
            ],
            'result_type': 'BatchCulturalEvolutionResults'
        }

    def save(self) -> Path:
        output_dir = self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "results.txt").write_text(str(self))

        filepath = output_dir / f"{self.FILENAME}{self.config.output_style.get_suffix()}"
        _save_json(filepath, self.serialise())
        return filepath

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchCulturalEvolutionResults':
        config = BatchCulturalEvolutionConfig(**data['config'])
        runs = [CulturalEvolutionResults.from_dict(rd) for rd in data['runs']]
        return cls(config=config, runs=runs)

    @classmethod
    def load(cls, output_dir: Path) -> 'BatchCulturalEvolutionResults':
        filepath = _find_file(Path(output_dir), cls.FILENAME)
        data = _load_json(filepath)
        if data.get('result_type') != 'BatchCulturalEvolutionResults':
            raise ValueError(
                f"Expected BatchCulturalEvolutionResults, got {data.get('result_type')}"
            )
        return cls.from_dict(data)
