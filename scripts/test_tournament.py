"""Run a fair tournament where all players play equal games."""
import logging
import sys
from pathlib import Path
import pandas as pd
import numpy as np

from emergent_llm.tournament import (BatchFairTournament, BatchFairTournamentConfig,
                                     BatchMixtureTournament, BatchMixtureTournamentConfig,
                                     BaseTournament, BaseTournamentConfig,
                                     FairTournament, MixtureTournament)
from emergent_llm.games.public_goods import PublicGoodsGame
from emergent_llm.games.collective_risk import CollectiveRiskGame
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription
from emergent_llm.players import SimplePlayer, LLMPlayer
from emergent_llm.common.actions import C, D
from emergent_llm.common.attitudes import COOPERATIVE, AGGRESSIVE

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fair_tournament.log'),
        logging.StreamHandler()
    ]
)

# def create_test_population():
#     """Create a test population where size is divisible by n_players."""
#     players = []

#     # 18 cooperative players
#     for i in range(18):
#         players.append(SimplePlayer(f"coop_{i}", lambda: C))

#     # 18 aggressive players
#     for i in range(18):
#         players.append(SimplePlayer(f"aggr_{i}", lambda: D))

#     return players

def create_test_population(game_description):
    """Create LLM players for testing."""
    cooperative_players = []

    # 18 LLM cooperative players
    for i in range(18):
        def cooperative_strategy(history):
            return lambda x: C

        cooperative_players.append(LLMPlayer(
            name=f"llm_coop_{i}",
            attitude=COOPERATIVE,
            game_description=game_description,
            strategy_class=cooperative_strategy,
        ))

    aggressive_players = []
    # 18 LLM aggressive players
    for i in range(18):
        def aggressive_strategy(history):
            return lambda x: D

        aggressive_players.append(LLMPlayer(
            name=f"llm_aggr_{i}",
            attitude=AGGRESSIVE,
            game_description=game_description,
            strategy_class=aggressive_strategy,
        ))

    return cooperative_players, aggressive_players

def run_fair_tournament(game_type, game_description):
    """Run tournament with Public Goods Game."""
    # Create game description

    # Create population (36 players = 6 matches)
    c_p, a_p = create_test_population(game_description)

    config = BaseTournamentConfig(game_type, game_description, repetitions=2)

    # Create and run tournament
    tournament = FairTournament(
        players=c_p + a_p,
        config=config
    )

    return tournament.run_tournament()

def run_mixture_tournament(game_type, game_description):
    """Run tournament with Public Goods Game."""
    # Create game description

    # Create population (36 players = 6 matches)
    c_p, a_p = create_test_population(game_description)

    config = BaseTournamentConfig(game_type, game_description, repetitions=2)

    # Create and run tournament
    tournament = MixtureTournament(
        cooperative_players=c_p,
        aggressive_players=a_p,
        config=config
    )

    return tournament.run_tournament()

def main():

    pgg_type = PublicGoodsGame
    pgg_description = PublicGoodsDescription(
        n_players=6,
        n_rounds=20,
        k=2.0
    )

    crd_type = CollectiveRiskGame
    crd_description = CollectiveRiskDescription(
        n_players=6,
        n_rounds=20,
        m=3,  # At least 3 cooperators needed
        k=2.0  # Reward if threshold met
    )

    """Run fair tournament."""
    print("Running Public Goods Tournament...")
    pgg_results = run_fair_tournament(pgg_type, pgg_description)

    # Analysis
    print("\n=== PUBLIC GOODS GAME RESULTS ===")
    print(pgg_results)

    print("\nRunning Collective Risk Tournament...")
    crd_results = run_fair_tournament(crd_type, crd_description)

    print("\n=== COLLECTIVE RISK DILEMMA RESULTS ===")
    print(crd_results)

    """Run mixture tournament."""
    print("Running Public Goods Tournament...")
    pgg_results = run_mixture_tournament(pgg_type, pgg_description)

    # Analysis
    print("\n=== PUBLIC GOODS GAME RESULTS ===")
    print(pgg_results)

    print("\nRunning Collective Risk Tournament...")
    crd_results = run_mixture_tournament(crd_type, crd_description)

    print("\n=== COLLECTIVE RISK DILEMMA RESULTS ===")
    print(crd_results)

    crd_results.create_schelling_diagram("/tmp/delete")

if __name__ == "__main__":
    main()
