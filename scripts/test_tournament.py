"""Run a fair tournament where all players play equal games."""
import logging

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
from emergent_llm.games import CollectiveRiskDescription, PublicGoodsDescription
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
        generator_name=generator_name
    )

    # Create and run tournament
    tournament = BatchMixtureTournament(
        collective_specs=[StrategySpec(Gene("", COLLECTIVE), CollectiveStrategy)]*16,
        exploitative_specs=[StrategySpec(Gene("", EXPLOITATIVE), ExploitativeStrategy)]*16,
        config=config
    )

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

    """Run fair tournament."""
    print("Running Public Goods Tournament...")
    pgg_results = run_fair_tournament(pgg_description)

    print("\n=== PUBLIC GOODS GAME RESULTS ===")
    print(pgg_results)

    pgg_results.save("./test/fair_pgg_results.json")
    check = FairTournamentResults.load("./test/fair_pgg_results.json")
    print(check)

    print("\nRunning Collective Risk Tournament...")
    crd_results = run_fair_tournament(crd_description)

    print("\n=== COLLECTIVE RISK DILEMMA RESULTS ===")
    print(crd_results)

    crd_results.save("./test/fair_crd_results.json")
    check = FairTournamentResults.load("./test/fair_crd_results.json")
    print(check)


    """Run mixture tournament."""
    print("Running Public Goods Tournament...")
    pgg_results = run_mixture_tournament(pgg_description)

    # Analysis
    print("\n=== PUBLIC GOODS GAME RESULTS ===")
    print(pgg_results)

    pgg_results.save("./test/mixture_pgg_results.json")
    check = MixtureTournamentResults.load("./test/mixture_pgg_results.json")
    print(check)

    check.create_schelling_diagram("./test/pgg_schelling.png")

    print("\nRunning Collective Risk Tournament...")
    crd_results = run_mixture_tournament(crd_description)

    print("\n=== COLLECTIVE RISK DILEMMA RESULTS ===")
    print(crd_results)

    crd_results.save("./test/mixture_crd_results.json")
    check = MixtureTournamentResults.load("./test/mixture_crd_results.json")
    print(check)

    crd_results.create_schelling_diagram("./test/crd_schelling.png")

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


if __name__ == "__main__":
    main()
