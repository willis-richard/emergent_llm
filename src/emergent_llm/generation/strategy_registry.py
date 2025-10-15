"""Registry for loading and sampling LLM-generated strategies."""
import importlib.util
import inspect
import random
from pathlib import Path

from emergent_llm.common import Attitude, Gene
from emergent_llm.players import BaseStrategy


class StrategyRegistry:
    """Loads and provides access to pre-generated strategies."""

    def __init__(self, strategies_dir: Path, game_name: str):
        """
        Initialize registry by loading all strategies for a game.

        Args:
            strategies_dir: Base strategies directory (e.g., Path("strategies"))
            game_name: Game subdirectory (e.g., "public_goods")
        """
        self.game_dir = strategies_dir / game_name
        if not self.game_dir.exists():
            raise ValueError(f"Game directory not found: {self.game_dir}")

        # Map (provider_model, attitude) -> list of strategy classes
        self.strategies: dict[tuple[str, Attitude], list[type[BaseStrategy]]] = {}

        self._load_all_strategies()

    def _load_all_strategies(self):
        """Load all strategy files in the game directory."""
        for strategy_file in self.game_dir.glob("*.py"):
            # Skip description files and __init__
            if "description" in strategy_file.name or strategy_file.name.startswith("__"):
                continue

            provider_model, strategies_by_attitude = self._load_file_by_attitude(strategy_file)

            # Store in registry
            for attitude, classes in strategies_by_attitude.items():
                key = (provider_model, attitude)
                self.strategies[key] = classes

    @classmethod
    def _load_file_by_attitude(cls, filepath: Path) -> tuple[str, dict[Attitude, list[type[BaseStrategy]]]]:
        """
        Load strategies from file and group by attitude.

        Args:
            filepath: Path to strategy file

        Returns:
            (provider_model, {attitude: [strategy_classes]})
        """
        provider_model = filepath.stem
        strategy_classes = cls._load_strategies_from_file(filepath)

        strategies_by_attitude = {}
        for attitude in [Attitude.COOPERATIVE, Attitude.AGGRESSIVE]:
            strategies_by_attitude[attitude] = [
                cls for cls in strategy_classes
                if attitude.name in cls.__name__
            ]

        return provider_model, strategies_by_attitude

    @staticmethod
    def _load_strategies_from_file(filepath: Path) -> list[type[BaseStrategy]]:
        """
        Load all strategy classes from a Python file.

        Args:
            filepath: Path to Python file containing strategies

        Returns:
            List of strategy classes found in file
        """
        spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Extract all BaseStrategy subclasses
        return [
            cls for name, cls in inspect.getmembers(module)
            if inspect.isclass(cls)
            and issubclass(cls, BaseStrategy)
            and cls != BaseStrategy
        ]

    @classmethod
    def load_file_as_tuples(cls, filepath: Path) -> tuple[list[tuple[Gene, type[BaseStrategy]]],
                                                           list[tuple[Gene, type[BaseStrategy]]]]:
        """
        Load strategies from a single file and pair with genes.

        Convenience method for batch tournaments that load one file.

        Args:
            filepath: Path to strategy file

        Returns:
            (cooperative_tuples, aggressive_tuples) where each tuple is (Gene, strategy_class)

        Raises:
            ValueError: If file doesn't exist
        """
        if not filepath.exists():
            raise ValueError(f"Strategy file not found: {filepath}")

        provider_model, strategies_by_attitude = cls._load_file_by_attitude(filepath)

        cooperative_tuples = [
            (Gene(provider_model, Attitude.COOPERATIVE), cls)
            for cls in strategies_by_attitude[Attitude.COOPERATIVE]
        ]

        aggressive_tuples = [
            (Gene(provider_model, Attitude.AGGRESSIVE), cls)
            for cls in strategies_by_attitude[Attitude.AGGRESSIVE]
        ]

        return cooperative_tuples, aggressive_tuples

    def sample_strategy(self, gene: Gene) -> type[BaseStrategy]:
        """
        Sample a random strategy for the given gene.

        Args:
            gene: Gene specifying provider_model and attitude

        Returns:
            Randomly sampled strategy class

        Raises:
            KeyError: If no strategies exist for this gene
        """
        key = (gene.provider_model, gene.attitude)
        if key not in self.strategies:
            raise KeyError(
                f"No strategies found for gene {gene}. "
                f"Available provider_models: {self.available_provider_models}"
            )

        strategies = self.strategies[key]
        if not strategies:
            raise KeyError(f"Empty strategy list for gene {gene}")

        return random.choice(strategies)

    @property
    def available_provider_models(self) -> set[str]:
        """Get set of all provider_models with loaded strategies."""
        return {provider_model for provider_model, _ in self.strategies.keys()}

    @property
    def available_genes(self) -> set[Gene]:
        """Get set of all genes with loaded strategies."""
        return {
            Gene(provider_model, attitude)
            for provider_model, attitude in self.strategies.keys()
        }

    def count_strategies(self, gene: Gene) -> int:
        """
        Count number of strategies available for a gene.

        Args:
            gene: Gene to check

        Returns:
            Number of strategies, or 0 if gene not found
        """
        key = (gene.provider_model, gene.attitude)
        return len(self.strategies.get(key, []))

    def validate_genes(self, genes: list[Gene]) -> None:
        """
        Validate that strategies exist for all genes.

        Args:
            genes: List of genes to validate

        Raises:
            ValueError: If any gene has no strategies
        """
        missing = []
        for gene in genes:
            key = (gene.provider_model, gene.attitude)
            if key not in self.strategies or not self.strategies[key]:
                missing.append(gene)

        if missing:
            raise ValueError(
                f"No strategies found for genes: {missing}\n"
                f"Available genes: {self.available_genes}"
            )

    def summary(self) -> str:
        """
        Get summary of loaded strategies.

        Returns:
            Human-readable summary string
        """
        lines = [
            f"Strategy Registry for {self.game_dir.name}",
            f"Provider models: {len(self.available_provider_models)}",
            f"Total genes: {len(self.strategies)}",
            "\nStrategies per gene:"
        ]

        for (provider_model, attitude), strategies in sorted(self.strategies.items()):
            gene = Gene(provider_model, attitude)
            lines.append(f"  {gene}: {len(strategies)} strategies")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"StrategyRegistry(game={self.game_dir.name}, genes={len(self.strategies)})"
