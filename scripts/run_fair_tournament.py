"""Run a fair tournament where all players play equal games."""
import logging
import sys
from pathlib import Path
import pandas as pd
import numpy as np

from emergent_llm.tournament.fair_tournament import FairTournament, FairTournamentConfig
from emergent_llm.games.public_goods import PublicGoodsGame
from emergent_llm.games.collective_risk import CollectiveRiskGame
from emergent_llm.games.game_description import PublicGoodsDescription, CollectiveRiskDescription
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

def create_test_population():
    """Create a test population where size is divisible by n_players."""
    players = []

    # 18 cooperative players
    for i in range(18):
        players.append(SimplePlayer(f"coop_{i}", lambda: C))

    # 18 aggressive players
    for i in range(18):
        players.append(SimplePlayer(f"aggr_{i}", lambda: D))

    return players

def create_llm_population():
    """Create LLM players for testing."""
    players = []

    # 18 LLM cooperative players
    for i in range(18):
        def cooperative_strategy(history):
            return C

        players.append(LLMPlayer(
            name=f"llm_coop_{i}",
            strategy_function=cooperative_strategy,
            attitude=COOPERATIVE,
            strategy_description="Always cooperate"
        ))

    # 18 LLM aggressive players
    for i in range(18):
        def aggressive_strategy(history):
            return D

        players.append(LLMPlayer(
            name=f"llm_aggr_{i}",
            strategy_function=aggressive_strategy,
            attitude=AGGRESSIVE,
            strategy_description="Always defect"
        ))

    return players

def run_public_goods_tournament():
    """Run tournament with Public Goods Game."""
    # Create tournament config
    config = FairTournamentConfig(
        n_players=6,
        n_rounds=20
    )

    # Create game description
    game_description = PublicGoodsDescription(
        n_players=6,
        n_rounds=20,
        k=2.0
    )

    # Create population (36 players = 6 matches)
    players = create_test_population()

    # Create and run tournament
    tournament = FairTournament(
        players=players,
        config=config,
        game_class=PublicGoodsGame,
        game_description=game_description
    )

    return tournament.run_tournament()

def run_collective_risk_tournament():
    """Run tournament with Collective Risk Dilemma."""
    # Create tournament config
    config = FairTournamentConfig(
        n_players=6,
        n_rounds=20
    )

    # Create game description - need at least 3 cooperators to get reward of 2
    game_description = CollectiveRiskDescription(
        n_players=6,
        n_rounds=20,
        m=3,  # At least 3 cooperators needed
        k=2.0  # Reward if threshold met
    )

    # Create population (36 players = 6 matches)
    players = create_test_population()

    # Create and run tournament
    tournament = FairTournament(
        players=players,
        config=config,
        game_class=CollectiveRiskGame,
        game_description=game_description
    )

    return tournament.run_tournament()

def main():
    """Run fair tournament."""
    print("Running Public Goods Tournament...")
    pgg_results = run_public_goods_tournament()
    pgg_results.to_csv('public_goods_results.csv', index=False)

    print("\nRunning Collective Risk Tournament...")
    crd_results = run_collective_risk_tournament()
    crd_results.to_csv('collective_risk_results.csv', index=False)

    # Analysis
    print("\n=== PUBLIC GOODS GAME RESULTS ===")
    analyze_results(pgg_results)

    print("\n=== COLLECTIVE RISK DILEMMA RESULTS ===")
    analyze_results(crd_results)

def analyze_results(results_df):
    """Analyze tournament results."""
    print("\nOverall Performance by Player Type:")
    type_summary = results_df.groupby('player_type')['payoff'].agg(['mean', 'std', 'count'])
    print(type_summary)

    print("\nGames played per player:")
    games_per_player = results_df.groupby('player_name').size()
    print(f"Min: {games_per_player.min()}, Max: {games_per_player.max()}")
    print(f"All players played same number of games: {games_per_player.nunique() == 1}")

    print(f"\nTotal matches: {results_df['match_id'].nunique()}")
    print(f"Total player-games: {len(results_df)}")

if __name__ == "__main__":
    main()
