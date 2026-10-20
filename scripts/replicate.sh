#!/bin/bash
# LLM replication experiment. Requires API keys.
# Run analyse.sh first: needs the diversity cache in $RESULTS_DIR/diversity/cache.
#
# Usage: scripts/replicate.sh [-r results_dir] [-s strategies_dir] [game ...]
# Games default to all of $GAMES. Re-running a finished (game, model) is a
# no-op: results.csv is resumed with the same seed.
set -e
source "$(dirname "$0")/config.sh"
shift $((OPTIND - 1))
if [ $# -gt 0 ]; then REPLICATE_GAMES=("$@"); else REPLICATE_GAMES=("${GAMES[@]}"); fi

for game in "${REPLICATE_GAMES[@]}"; do
    pids=()
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
               --n_episodes 100 > /dev/null &
        pids+=($!)
    done
    # Plain `wait` returns 0 even if a job failed; wait on each pid instead.
    for pid in "${pids[@]}"; do wait "$pid"; done
done

python scripts/build_fidelity_table.py --results_dir "$RESULTS_DIR"
