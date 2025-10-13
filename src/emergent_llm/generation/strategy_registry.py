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

            # Extract provider_model from filename
            # e.g., "anthropic_claude-sonnet-4.py" -> "anthropic_claude-sonnet-4"
            provider_model = strategy_file.stem

            # Load the module
            strategy_classes = self._load_strategies_from_file(strategy_file)

            # Group by attitude
            for attitude in [Attitude.COOPERATIVE, Attitude.AGGRESSIVE]:
                key = (provider_model, attitude)
                self.strategies[key] = [
                    cls for cls in strategy_classes
                    if attitude.name in cls.__name__  # e.g., "Strategy_COOPERATIVE_1"
                ]

    def _load_strategies_from_file(self, filepath: Path) -> list[type[BaseStrategy]]:
        """Load all strategy classes from a Python file."""
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
            raise KeyError(f"No strategies found for {gene}")

        strategies = self.strategies[key]
        if not strategies:
            raise KeyError(f"Empty strategy list for {gene}")

        return random.choice(strategies)

    @property
    def available_provider_models(self) -> set[str]:
        """Get set of all provider_models with loaded strategies."""
        return {provider_model for provider_model, _ in self.strategies.keys()}

    def validate_genes(self, genes: list[Gene]) -> None:
        """
        Validate that strategies exist for all genes.

        Raises:
            ValueError: If any gene has no strategies
        """
        missing = []
        for gene in genes:
            key = (gene.provider_model, gene.attitude)
            if key not in self.strategies or not self.strategies[key]:
                missing.append(gene)

        if missing:
            raise ValueError(f"No strategies found for genes: {missing}")
