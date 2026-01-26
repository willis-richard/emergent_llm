#!/bin/bash
#SBATCH --job-name=pca-gen
#SBATCH --partition=workq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail


mkdir -p logs



# ---- 系统库 ----
module purge
module load cuda/12.6




source ~/miniforge3/bin/activate
conda activate emergent_llm
cd $HOME/emergent_llm
export PYTHONPATH=$(pwd)
# ---- PCA baseline: plot multiple models on one figure per game ----
# GAMES=("public_goods" "collective_risk" "common_pool")  # add "collective_risk" "common_pool" if needed
# MODELS=(
#   "gemini-2.5-flash"
#   "gpt-5-mini"
#   "llama3.1-70b"
#   "mistral-latest"
#   "claude-haiku-4-5"
#   "deepseek-r1-distill-llama-70b"
# )

python -u scripts/diversity.py \
  --games public_goods_prompt \
  --strategies_dir strategies \
  --n_players 4 \
  --n_rounds 5 \
  --n_games 2 \
  --n_processes 1 \
  --results_dir results \
  --models "deepseek-r1-distill-llama-70b" "claude-haiku-4-5" \
  --recompute \
  --feature_mode baseline_opponents 
####################################
# 13.  
####################################
echo "=============================================="
echo "✅ JOB FINISHED at $(date)"
