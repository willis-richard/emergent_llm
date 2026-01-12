"""Run a fair tournament where all players play equal games."""
import logging
from pathlib import Path

from emergent_llm.common import (
    COLLECTIVE,
    EXPLOITATIVE,
    C,
    D,
    GameDescription,
    GameState,
    Gene,
    PlayerHistory,
)
from emergent_llm.games import CollectiveRiskDescription, PublicGoodsDescription, CommonPoolDescription
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import BaseStrategy, LLMPlayer, StrategySpec
from emergent_llm.tournament import (
    BaseTournamentConfig,
    BatchFairTournament,
    BatchFairTournamentResults,
    BatchMixtureTournament,
    BatchMixtureTournamentResults,
    BatchTournamentConfig,
    FairTournament,
    FairTournamentResults,
    MixtureTournament,
    MixtureTournamentResults,
    CulturalEvolutionConfig,
    CulturalEvolution,
    CulturalEvolutionResults,
    BatchCulturalEvolutionConfig,
    BatchCulturalEvolution,
    BatchCulturalEvolutionResults
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fair_tournament.log'),
        logging.StreamHandler()
    ]
)


class CollectiveStrategy(BaseStrategy):
    def __init__(self, game_description):
        pass

    def __call__(self, state, history):
        return C


class ExploitativeStrategy(BaseStrategy):
    def __init__(self, game_description):
        pass

    def __call__(self, state, history):
        return D


def create_test_population(game_description):
    """Create LLM players for testing."""
    collective_players = []

    for i in range(18):
        collective_players.append(LLMPlayer(
            name=f"llm_coop_{i}",
            gene=Gene("", COLLECTIVE),
            game_description=game_description,
            strategy_class=CollectiveStrategy,
        ))

    exploitative_players = []
    for i in range(18):
        exploitative_players.append(LLMPlayer(
            name=f"llm_aggr_{i}",
            gene=Gene("", EXPLOITATIVE),
            game_description=game_description,
            strategy_class=ExploitativeStrategy,
        ))

    return collective_players, exploitative_players

def run_fair_tournament(game_description):
    """Run tournament with Public Goods Game."""
    # Create population (36 players = 6 matches)
    c_p, a_p = create_test_population(game_description)

    config = BaseTournamentConfig(game_description, repetitions=2, processes=2)

    # Create and run tournament
    tournament = FairTournament(
        players=c_p + a_p,
        config=config
    )

    return tournament.run_tournament()

def run_mixture_tournament(game_description):
    """Run tournament with Public Goods Game."""
    # Create population (36 players = 6 matches)
    c_p, a_p = create_test_population(game_description)


    config = BaseTournamentConfig(game_description, repetitions=2, processes=2)

    # Create and run tournament
    tournament = MixtureTournament(
        collective_players=c_p,
        exploitative_players=a_p,
        config=config
    )

    return tournament.run_tournament()

def run_batch_fair_tournament(generator_name):
    """Run tournament with Public Goods Game."""
    config = BatchTournamentConfig(
        group_sizes=[2,4,8],
        repetitions=2,
        processes=2,
        results_dir="./test",
        compress=False,
        generator_name=generator_name
    )

    strategies = [CollectiveStrategy] * 16 + [ExploitativeStrategy] * 16
    genes = [Gene("", COLLECTIVE)] * 16 + [Gene("", EXPLOITATIVE)] * 16

    # Create and run tournament
    tournament = BatchFairTournament(
        strategies=[StrategySpec(g, s) for g, s in zip(genes, strategies)],
        config=config
    )

    return tournament.run_tournament()

def run_batch_mixture_tournament(generator_name):
    """Run tournament with Public Goods Game."""
    config = BatchTournamentConfig(
        group_sizes=[2,4,8],
        repetitions=2,
        processes=2,
        results_dir="./test",
        compress=False,
        generator_name=generator_name
    )

    # Create and run tournament
    tournament = BatchMixtureTournament(
        collective_specs=[StrategySpec(Gene("", COLLECTIVE), CollectiveStrategy)]*16,
        exploitative_specs=[StrategySpec(Gene("", EXPLOITATIVE), ExploitativeStrategy)]*16,
        config=config
    )

    return tournament.run_tournament()

def create_ce_config(game_description : GameDescription):
    return CulturalEvolutionConfig(game_description,
                                   population_size=18,
                                   top_k=4,
                                   mutation_rate=0.1,
                                   threshold_pct=0.8,
                                   max_generations=5,
                                   repetitions_per_generation=2)

def run_cultural_evolution(game_description: GameDescription):
    """Run tournament with Public Goods Game."""
    # Create population (36 players = 6 matches)
    config = create_ce_config(game_description)

    registry = StrategyRegistry(
        strategies_dir=Path("strategies"),
        game_name="common_pool",
    )

    # Create and run tournament
    tournament = CulturalEvolution(config, registry)

    return tournament.run_tournament()

def run_batch_cultural_evolution(game_description):
    config = BatchCulturalEvolutionConfig(create_ce_config(game_description),
                                          n_runs=2,
                                          n_processes=2,
                                          results_dir="test",
                                          compress=False,
                                          strategies_dir="strategies",
                                          game_name="public_goods")

    tournament = BatchCulturalEvolution(config)

    return tournament.run_tournament()

def main():

    pgg_description = PublicGoodsDescription(
        n_players=6,
        n_rounds=20,
        k=2.0
    )

    crd_description = CollectiveRiskDescription(
        n_players=6,
        n_rounds=20,
        m=3,  # At least 3 cooperators needed
        k=2.0  # Reward if threshold met
    )

    cpr_description = CommonPoolDescription(
        n_players=6,
        n_rounds=20,
        capacity=36
    )

    """Run fair tournament."""
    print("Running Fair Public Goods Tournament...")
    pgg_results = run_fair_tournament(pgg_description)
    print(pgg_results)
    pgg_results.save("./test/fair_pgg_results.json")

    check = FairTournamentResults.load("./test/fair_pgg_results.json")
    print(check)


    """Run mixture tournament."""
    print("\nRunning Mixture Collective Risk Tournament...")
    crd_results = run_mixture_tournament(crd_description)
    print(crd_results)
    crd_results.save("./test/mixture_crd_results.json")

    check = MixtureTournamentResults.load("./test/mixture_crd_results.json")
    print(check)

    crd_results.create_schelling_diagram("./test/crd_schelling")

    print("\n=== BATCH FAIR CPR ===")
    b_cpr_results = run_batch_fair_tournament("common_pool_default")
    print(b_cpr_results)
    b_cpr_results.save()

    check = BatchFairTournamentResults.load("./test/batch_fair/results.json")
    print(check)

    print("\n=== BATCH MIXTURE CPR ===")
    b_cpr_results = run_batch_mixture_tournament("common_pool_default")
    print(b_cpr_results)
    b_cpr_results.save()

    check = BatchMixtureTournamentResults.load("./test/batch_mixture/results.json")
    print(check)

    b_cpr_results.create_schelling_diagrams()
    b_cpr_results.create_relative_schelling_diagram()
    b_cpr_results.create_social_welfare_diagram()

    print("\n=== CULTURAL EVOLUTION CPR ===")
    ce_results = run_cultural_evolution(cpr_description)
    print(ce_results)
    ce_results.save("./test/ce_results.json")

    check = CulturalEvolutionResults.load("./test/ce_results.json")
    print(check)

    print("\n=== BATCH CULTURAL EVOLUTION PGG ===")
    bce_results = run_batch_cultural_evolution(pgg_description)
    print(bce_results)
    bce_results.save()

    check = BatchCulturalEvolutionResults.load("./test/cultural_evolution/public_goods/n6_r20_pop18_top4_mut0.1_thr0.8_gen5_rep2/results.json")
    print(check)

if __name__ == "__main__":
    main()
