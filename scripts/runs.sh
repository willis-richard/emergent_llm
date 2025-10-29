#!/bin/bash

# Define variables
GAMES=("public_goods" "collective_risk" "common_pool")
PROVIDER_MODELS=(
    "openai gpt-5-mini"
    "anthropic claude-sonnet-4-0"
    "google gemini-2.5-flash-lite"
)

# for game in "${GAMES[@]}"; do
#     for pm in "${PROVIDER_MODELS[@]}"; do
#         read provider model <<< "$pm"

#         python src/emergent_llm/generation/create_strategies.py descriptions \
#                 --llm_provider "$provider" \
#                 --model_name "$model" \
#                 --game "$game" \
#                 --n 128 &
#     done
#     wait
# done

# for game in "${GAMES[@]}"; do
#     for pm in "${PROVIDER_MODELS[@]}"; do
#         read provider model <<< "$pm"

#         python src/emergent_llm/generation/create_strategies.py implementations \
#                    --llm_provider "$provider" \
#                    --model_name "$model" \
#                    --game "$game" &
#     done
#     wait
# done

# for game in "${GAMES[@]}"; do
#     for pm in "${PROVIDER_MODELS[@]}"; do
#         read provider model <<< "$pm"

#         python scripts/run_tournament.py \
#                --strategies strategies/$game/${model}.py \
#                --game $game \
#                --matches 200 \
#                --group-sizes 4 16 64 &
#     done
#     wait
# done

for game in "${GAMES[@]}"; do
    python scripts/run_cultural_evolution.py --game common_pool --n_players 16 --population_size 128 --n_rounds 20 --top_k 16 --repetitions 4 --n_runs 4 --n_processes 4 --max_generations 20
done
