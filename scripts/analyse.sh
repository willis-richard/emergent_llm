#!/bin/bash
# Reproduces all simulation results from the deposited strategies. No API access needed.
set -e
source "$(dirname "$0")/config.sh"

python scripts/diversity.py \
        --strategies_dir "$STRATEGIES_DIR" \
        --n_rounds 7 \
        --n_games 30 \
        --n_processes $N_PROCESSES \
        --plot_baselines \
        --results_dir "$RESULTS_DIR"

pids=()
for pm in "${PROVIDER_MODELS[@]}"; do
    read provider model <<< "$pm"
    for game in "${GAMES[@]}"; do
        # Enums cannot be pickled - parallelise across processes, not within the script
        pids=( $(for p in "${pids[@]}"; do kill -0 "$p" 2>/dev/null && echo "$p"; done) )
        while [ ${#pids[@]} -ge $N_PROCESSES ]; do
            sleep 2
            pids=( $(for p in "${pids[@]}"; do kill -0 "$p" 2>/dev/null && echo "$p"; done) )
        done
        python scripts/run_tournament.py \
                --strategies "$STRATEGIES_DIR/$game/${model}.py" \
                --game "$game" \
                --matches 200 \
                --group-sizes 4 16 64 256 \
                --n_processes 1 \
                --results_dir "$RESULTS_DIR" \
                --output_style summary &
        pids+=($!)
    done
done
wait

python scripts/plot_combined_social_welfare.py \
        --results_dir "$RESULTS_DIR/self_play" \
        --output_dir "$RESULTS_DIR/diagrams" \
        --n_se 1.96

# Cultural evolution: main results (beta=1, G=4) then Appendix C sensitivity.
# Format: "beta games_per_agent subdir"
EVOLUTION_CONFIGS=(
    "1 4 evolution_main"
    "1 16 evolution_G16"
    "0.25 4 evolution_beta0.25"
    "4 4 evolution_beta4"
)

for cfg in "${EVOLUTION_CONFIGS[@]}"; do
    read beta g subdir <<< "$cfg"
    for game in "${GAMES[@]}"; do
        for n_players in "${EVOLUTION_PLAYERS[@]}"; do
            python scripts/run_cultural_evolution.py \
                   --game ${game} \
                   --n_players $n_players \
                   --n_rounds 20 \
                   --population_size 512 \
                   --beta $beta \
                   --mutation_rate 0.0025 \
                   --n_generations 1000 \
                   --final_window 100 \
                   --games_per_agent $g \
                   --n_runs 100 \
                   --n_processes $N_PROCESSES \
                   --strategies_dir "$STRATEGIES_DIR" \
                   --results_dir "$RESULTS_DIR/$subdir" \
                   --output_style summary
        done
    done
done
