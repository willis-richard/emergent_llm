#!/bin/bash

RESULTS_DIR="results"
STRATEGIES_DIR="strategies"
N_PROCESSES=1

while getopts "r:s:n:" opt; do
    case "$opt" in
        r) RESULTS_DIR="$OPTARG" ;;
        s) STRATEGIES_DIR="$OPTARG" ;;
        n) N_PROCESSES="$OPTARG" ;;
        *) exit 1 ;;
    esac
done

GAMES=("public_goods" "collective_risk" "common_pool")
PROVIDER_MODELS=(
    "openai gpt-5-mini"
    "google gemini-2.5-flash"
    "anthropic claude-haiku-4-5"
    "ollama llama3.1-70b"
    "ollama mistral:7b.py"
)
EVOLUTION_PLAYERS=(4 64)

# for game in "${GAMES[@]}"; do
#     for pm in "${PROVIDER_MODELS[@]}"; do
#         read provider model <<< "$pm"
#         (
#             python src/emergent_llm/generation/create_strategies.py \
#                    --llm_provider "$provider" \
#                    --model_name "$model" \
#                    --game "$game" \
#                    --strategies_dir "$STRATEGIES_DIR" \
#                    descriptions \
#                    --n 512

#             python src/emergent_llm/generation/create_strategies.py \
#                    --llm_provider "$provider" \
#                    --model_name "$model" \
#                    --game "$game" \
#                    --strategies_dir "$STRATEGIES_DIR" \
#                    implementations \
#                    --max_retries 5
#         ) &
#     done
#     wait
# done

python scripts/diversity.py \
        --strategies_dir "$STRATEGIES_DIR" \
        --n_rounds 5 \
        --n_games 50 \
        --n_processes $N_PROCESSES \
        --results_dir "$RESULTS_DIR"

for game in "${GAMES[@]}"; do
    for pm in "${PROVIDER_MODELS[@]}"; do
        read provider model <<< "$pm"

        python scripts/run_tournament.py \
               --strategies "$STRATEGIES_DIR/$game/${model}.py" \
               --game $game \
               --matches 200 \
               --group-sizes 4 16 64 256 \
               --n_processes $N_PROCESSES \
               --results_dir "$RESULTS_DIR" \
               --output_style summary \
               --verbose
    done
done

for game in "${GAMES[@]}"; do
    for n_players in "${EVOLUTION_PLAYERS[@]}"; do
        python scripts/run_cultural_evolution.py \
               --game ${game} \
               --n_players $n_players \
               --n_rounds 20 \
               --population_size 512 \
               --top_k 64 \
               --mutation_rate 0.1 \
               --threshold_percent 0.75 \
               --max_generations 200 \
               --repetitions 10 \
               --n_runs 100 \
               --n_processes $N_PROCESSES \
               --results_dir "$RESULTS_DIR" \
               --output_style summary
    done
done
