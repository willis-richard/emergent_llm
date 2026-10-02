#!/bin/bash
# LLM replication experiment. Requires API keys.
# Run analyse.sh first: needs the diversity cache in $RESULTS_DIR/diversity/cache.
set -e
source "$(dirname "$0")/config.sh"

for game in "${GAMES[@]}"; do
    for pm in "${PROVIDER_MODELS[@]}"; do
        read provider model <<< "$pm"
        python scripts/replicate_strategies.py \
               --game ${game} \
               --llm_provider ${provider} \
               --strategy_model ${model} \
               --inference_model ${model} \
               --strategies_dir "$STRATEGIES_DIR" \
               --results_dir "$RESULTS_DIR" \
               --seed 0 \
               --n_episodes 100 &
    done
    wait
done
