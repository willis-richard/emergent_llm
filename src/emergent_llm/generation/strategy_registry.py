"""Registry for loading and sampling LLM-generated strategies."""
import importlib.util
import inspect
import random
from pathlib import Path

from emergent_llm.common import Attitude, Gene
from emergent_llm.players import BaseStrategy, StrategySpec


class StrategyRegistry:
    """Registry of StrategySpecs (gene + strategy class pairs)."""

    def __init__(self, strategies_dir: Path, game_name: str):
        self.game_dir = strategies_dir / game_name
        if not self.game_dir.exists():
            raise ValueError(f"Game directory not found: {self.game_dir}")

        # Store StrategySpecs directly, keyed by Gene
        self.strategies: dict[Gene, list[StrategySpec]] = {}
        self._load_all_strategies()

    def _load_all_strategies(self):
        """Load all strategy files in the game directory."""
        for strategy_file in self.game_dir.glob("*.py"):
            if "description" in strategy_file.name or strategy_file.name.startswith("__"):
                continue

            specs = self._load_specs_from_file(strategy_file)

            # Group by gene
            for spec in specs:
                if spec.gene not in self.strategies:
                    self.strategies[spec.gene] = []
                self.strategies[spec.gene].append(spec)

    @classmethod
    def _load_specs_from_file(cls, filepath: Path) -> list[StrategySpec]:
        """Load all StrategySpecs from a Python file."""
        provider_model = filepath.stem
        strategy_classes = cls._load_strategies_from_file(filepath)

        specs = []
        for strategy_class in strategy_classes:
            # Extract attitude from class name (Strategy_COOPERATIVE_1)
            if "COOPERATIVE" in strategy_class.__name__:
                attitude = Attitude.COOPERATIVE
            elif "AGGRESSIVE" in strategy_class.__name__:
                attitude = Attitude.AGGRESSIVE
            else:
                continue  # Skip malformed classes

            gene = Gene(provider_model, attitude)
            specs.append(StrategySpec(gene, strategy_class))

        return specs

    @staticmethod
    def _load_strategies_from_file(filepath: Path) -> list[type[BaseStrategy]]:
        """Load all strategy classes from a Python file."""
        spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return [
            cls for name, cls in inspect.getmembers(module)
            if inspect.isclass(cls)
            and issubclass(cls, BaseStrategy)
            and cls != BaseStrategy
        ]

    @classmethod
    def load_file(cls, filepath: Path) -> tuple[list[StrategySpec], list[StrategySpec]]:
        """
        Load strategies from a single file, split by attitude.

        Convenience method for batch tournaments that load one file.
        """
        if not filepath.exists():
            raise ValueError(f"Strategy file not found: {filepath}")

        all_specs = cls._load_specs_from_file(filepath)

        cooperative = [s for s in all_specs if s.gene.attitude == Attitude.COOPERATIVE]
        aggressive = [s for s in all_specs if s.gene.attitude == Attitude.AGGRESSIVE]

        return cooperative, aggressive

    def sample_spec(self, gene: Gene) -> StrategySpec:
        """
        Sample a random StrategySpec for the given gene.

        Returns:
            Randomly sampled StrategySpec
        """
        if gene not in self.strategies:
            raise KeyError(
                f"No strategies found for gene {gene}. "
                f"Available genes: {self.available_genes}"
            )

        specs = self.strategies[gene]
        if not specs:
            raise KeyError(f"Empty strategy list for gene {gene}")

        return random.choice(specs)

    def get_all_specs(self, gene: Gene) -> list[StrategySpec]:
        """Get all StrategySpecs for a given gene."""
        return self.strategies.get(gene, [])

    @property
    def available_genes(self) -> set[Gene]:
        """Get set of all genes with loaded strategies."""
        return set(self.strategies.keys())

    @property
    def available_provider_models(self) -> set[str]:
        """Get set of all provider models with loaded strategies."""
        return set(gene.provider_model for gene in self.available_genes)

    def count_strategies(self, gene: Gene) -> int:
        """Count number of strategies available for a gene."""
        return len(self.strategies.get(gene, []))
