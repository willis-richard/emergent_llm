#!/bin/bash
# Generates new strategies via LLM APIs. Requires API keys.
# This does NOT reproduce the paper's strategies; those are deposited in strategies/.
set -e
source "$(dirname "$0")/config.sh"

for game in "${GAMES[@]}"; do
    for pm in "${PROVIDER_MODELS[@]}"; do
        read provider model <<< "$pm"
        (
            python src/emergent_llm/generation/create_strategies.py \
                   --llm_provider "$provider" \
                   --model_name "$model" \
                   --game "$game" \
                   --strategies_dir "$STRATEGIES_DIR" \
                   --full_attitudes \
                   descriptions \
                   --n 128

            python src/emergent_llm/generation/create_strategies.py \
                   --llm_provider "$provider" \
                   --model_name "$model" \
                   --game "$game" \
                   --strategies_dir "$STRATEGIES_DIR" \
                   implementations \
                   --max_retries 5
        ) &
    done
    wait
done
