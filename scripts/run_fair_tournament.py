"""Run a fair tournament where all players play equal games."""
import logging
import sys
from pathlib import Path
import pandas as pd

from emergent_llm.tournament.fair_tournament import FairTournament, FairTournamentConfig
from emergent_llm.games.public_goods import PublicGoodsGame
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

def main():
    """Run fair tournament."""
    # Create tournament config
    config = FairTournamentConfig(
        n_players=6,
        n_rounds=20
    )

    # Create population (36 players = 6 matches)
    players = create_test_population()  # or create_llm_population()

    # Create and run tournament
    tournament = FairTournament(
        players=players,
        config=config,
        game_class=PublicGoodsGame,
        game_kwargs={'k': 2.0}
    )

    # Run tournament
    results_df = tournament.run_tournament()

    # Save results
    results_df.to_csv('fair_tournament_results.csv', index=False)

    # Basic analysis
    print("\nOverall Performance by Player Type:")
    type_summary = results_df.groupby('player_type')['payoff'].agg(['mean', 'std', 'count'])
    print(type_summary)

    print("\nGames played per player:")
    games_per_player = results_df.groupby('player_name').size()
    print(f"Min: {games_per_player.min()}, Max: {games_per_player.max()}")
    print(f"All players played same number of games: {games_per_player.nunique() == 1}")

    print(f"\nTotal matches: {results_df['match_id'].nunique()}")
    print(f"Total player-games: {len(results_df)}")

    # Additional analysis using history data
    print("\nHistory Analysis:")
    analyze_tournament_history(tournament)

def analyze_tournament_history(tournament):
    """Analyze historical data from tournament results."""
    total_cooperation_rate = 0
    total_rounds = 0

    for result in tournament.results:
        history = result.game_result.history
        if history.actions.size > 0:
            # Calculate cooperation rate for this match
            cooperation_count = np.sum(history.actions == C)
            total_actions = history.actions.size
            match_coop_rate = cooperation_count / total_actions

            print(f"Match {result.match_id}: {match_coop_rate:.2%} cooperation")

            total_cooperation_rate += cooperation_count
            total_rounds += total_actions

    if total_rounds > 0:
        overall_coop_rate = total_cooperation_rate / total_rounds
        print(f"Overall cooperation rate: {overall_coop_rate:.2%}")

if __name__ == "__main__":
    main()
