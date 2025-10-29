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

for game in "${GAMES[@]}"; do
    for pm in "${PROVIDER_MODELS[@]}"; do
        read provider model <<< "$pm"

        python scripts/run_tournament.py \
               --strategies strategies/$game/${provider}_${model}.py \
               --game $game \
               --matches 200 \
               --group-sizes 4 16 64 &
    done
    wait
done
