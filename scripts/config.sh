#!/bin/bash
# Shared settings, sourced by generate.sh, analyse.sh and replicate.sh

RESULTS_DIR="results"
STRATEGIES_DIR="strategies"
N_PROCESSES=1
BETA=1
GAMES_PER_AGENT=4

GAMES=("public_goods" "collective_risk" "common_pool")
PROVIDER_MODELS=(
    "openai gpt-5.4-mini"
    "google gemini-3.1-flash-lite-preview"
    "anthropic claude-haiku-4-5"
)
EVOLUTION_PLAYERS=(4 64)

while getopts "r:s:n:b:g:" opt; do
    case "$opt" in
        r) RESULTS_DIR="$OPTARG" ;;
        s) STRATEGIES_DIR="$OPTARG" ;;
        n) N_PROCESSES="$OPTARG" ;;
        *) exit 1 ;;
    esac
done
