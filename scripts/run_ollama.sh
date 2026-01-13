#!/bin/bash
#SBATCH --job-name=ollama-gen
#SBATCH --partition=workq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail
# cd "${SLURM_SUBMIT_DIR}"
# # ---- TMPDIR fix (avoid /local/user/*) ----
# export TMPDIR="/tmp/${USER}/${SLURM_JOB_ID}"
# mkdir -p "${TMPDIR}"

mkdir -p logs
nvidia-smi


# ---- 系统库 ----
module purge
module load cuda/12.6

export OLLAMA_BIN="$HOME/ollama-arm64/bin/ollama"
export OLLAMA_MODELS="/projects/a5l/jianing/.ollama/models"
mkdir -p "$OLLAMA_MODELS"

export OLLAMA_HOST="http://127.0.0.1:11434"
unset PMI_RANK PMI_SIZE PMI_FD

echo "ARCH: $(uname -m)"
file "$OLLAMA_BIN"
"$OLLAMA_BIN" --version

LOG_FILE="logs/ollama-serve-${SLURM_JOB_ID}.log"
echo "Starting ollama server... log=${LOG_FILE}"
"$OLLAMA_BIN" serve > "${LOG_FILE}" 2>&1 &
SERVER_PID=$!
trap "kill $SERVER_PID 2>/dev/null || true" EXIT INT TERM

for i in {1..120}; do
  curl -fsS "http://127.0.0.1:11434/api/tags" >/dev/null 2>&1 && break
  sleep 1
done




source ~/miniforge3/bin/activate
conda activate emergent_llm
cd $HOME/emergent_llm
export PYTHONPATH=$(pwd)
# ---- 你的原始逻辑（已修正 --game_name）----
GAMES=("public_goods")
PROVIDER_MODELS=(
    "ollama mistral:latest"
    "ollama llama3.1:70b"
    "ollama deepseek-r1:32b"
)
# ollama pull deepseek-r1:32b
# ollama pull mistral:latest
# ollama pull llama3.1:70b

for game in "${GAMES[@]}"; do
  for pm in "${PROVIDER_MODELS[@]}"; do
    read provider model <<< "$pm"
    (
      python -u src/emergent_llm/generation/create_strategies.py descriptions \
        --llm_provider "$provider" \
        --model_name "$model" \
        --game_name "$game" \
        --n 600

      python -u src/emergent_llm/generation/create_strategies.py implementations \
        --llm_provider "$provider" \
        --model_name "$model" \
        --game_name "$game" \
        --max_retries 5
    ) 
  done
  wait
done

####################################
# 13. 安全关闭 Ollama
####################################
echo "=============================================="
echo "🛑 Killing Ollama server..."
kill $SERVER_PID || echo "Ollama already stopped"

echo "✅ JOB FINISHED at $(date)"

