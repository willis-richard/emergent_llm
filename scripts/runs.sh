#!/bin/bash

GAMES=("public_goods" "collective_risk" "common_pool")
PROVIDER_MODELS=(
    "openai gpt-5-mini"
    "google gemini-2.5-flash"
    "anthropic claude-haiku-4-5"
)
EVOLUTION_PLAYERS=(4 64)

# for game in "${GAMES[@]}"; do
#     for pm in "${PROVIDER_MODELS[@]}"; do
#         read provider model <<< "$pm"
#         (
#             python src/emergent_llm/generation/create_strategies.py descriptions \
#                    --llm_provider "$provider" \
#                    --model_name "$model" \
#                    --game "$game" \
#                    --n 512

#             python src/emergent_llm/generation/create_strategies.py implementations \
#                    --llm_provider "$provider" \
#                    --model_name "$model" \
#                    --game "$game" \
#                    --max_retries 5
#         ) &
#     done
#     wait
# done

# python scripts/diversity.py \
#         --game $game \
#         --strategies_dir strategies \
#         --models claude-haiku-4-5 gpt-5-mini gemini-2.5-flash \
#         --n_rounds 5 \
#         --n_games 20 \
#         --n_processes 4

# for game in "${GAMES[@]}"; do
#     for pm in "${PROVIDER_MODELS[@]}"; do
#         read provider model <<< "$pm"

#         python scripts/run_tournament.py \
    #                --strategies strategies/$game/${model}.py \
    #                --game $game \
    #                --matches 200 \
    #                --group-sizes 4 16 64 256 \
    #                --processes 1 \
    #                --verbose &
#     done
#     wait
# done

for game in "${GAMES[@]}"; do
    for n_players in "${EVOLUTION_PLAYERS[@]}"; do
        python scripts/run_cultural_evolution.py \
            --game ${game} \
            --n_players $n_players \
            --n_rounds 20 \
            --population_size 512 \
            --top_k 64 \
            --repetitions 10 \
            --n_runs 100 \
            --n_processes 4 \
            --max_generations 200
    done
done
