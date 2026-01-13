#!/bin/bash

GAMES=("public_goods" "collective_risk" "common_pool")
PROVIDER_MODELS=(
    "openai gpt-5-mini"
    "google gemini-2.5-flash"
    "anthropic claude-haiku-4-5"
)
EVOLUTION_PLAYERS=(4 64)
PROCESSES=4

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
#         --strategies_dir strategies \
#         --n_rounds 5 \
#         --n_games 50 \
#         --n_processes $PROCESSES

for game in "${GAMES[@]}"; do
    for pm in "${PROVIDER_MODELS[@]}"; do
        read provider model <<< "$pm"

        # python scripts/run_tournament.py \
        #        --strategies strategies/$game/${model}.py \
        #        --game $game \
        #        --matches 200 \
        #        --group-sizes 4 16 64 256 \
        #        --processes $PROCESSES \
        #        --output_style summary \
        #        --verbose
    done
done

for game in "${GAMES[@]}"; do
    for n_players in "${EVOLUTION_PLAYERS[@]}"; do
        # python scripts/run_cultural_evolution.py \
        #        --game ${game} \
        #        --n_players $n_players \
        #        --n_rounds 20 \
        #        --population_size 512 \
        #        --top_k 64 \
        #        --mutation_rate 0.1 \
        #        --threshold_percent 0.75 \
        #        --max_generations 200 \
        #        --repetitions 10 \
        #        --n_runs 100 \
        #        --n_processes $PROCESSES \
        #        --output_style summary

        python scripts/run_cultural_evolution.py \
               --game ${game} \
               --n_players $n_players \
               --n_rounds 3 \
               --population_size 128 \
               --top_k 16 \
               --repetitions 2 \
               --n_runs 10 \
               --n_processes $PROCESSES \
               --max_generations 20
    done
done
