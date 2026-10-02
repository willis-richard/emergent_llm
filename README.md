# Social Dilemma Experiments

A benchmark for assessing LLM behaviour in multi-player social dilemma games, investigating whether large language models exhibit differential capabilities with exploitative vs collective strategies.

## Overview

This project investigates the emergent behaviour of LLM-driven autonomous agents in multi-agent social dilemmas. The key research question is whether LLMs are more successful with exploitative strategies compared to collective, cooperative approaches, and what this means for potential negative social outcomes.

### Key Features

- **Strategy Generation**: LLMs generate strategies in natural language, then implement them as Python functions
- **Multiple Games**: Support for Public Goods Game (PGG), Collective Risk Dilemma (CRD) and Common Pool Resource (CPR)
- **Comprehensive Logging**: Detailed game histories and strategy performance metrics
- **Attitude-Based Analysis**: Compare collective vs exploitative strategy performance
- **Code Safety**: Restricted execution environment for LLM-generated strategies

## Installation

### Prerequisites
- Python 3.11
- Conda or Miniconda

### Steps

1. Clone the repository:
```bash
git clone https://github.com/willis-richard/emergent_llm.git
cd emergent_llm
```

2. Install
```bash
conda env update -f environment.yml
conda activate emergent_llm
```

## Strategy Generation

The generated strategies are in [strategies](./strategies). To generate new ones use:


```bash
python3 src/emergent_llm/generation/create_strategies.py --llm_provider <provider> --model_name <model_name> --game <game> descriptions --n <number_of_strategies>
python3 src/emergent_llm/generation/create_strategies.py --llm_provider <provider> --model_name <model_name> --game <game> implementations --n <number_of_strategies>
```

You will need LLM APIs. Set the relevant keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, or `OLLAMA_HOST`.

### Representative Strategies

The strategies that are closest to the PCA centroid means are saved in [representative_strategies](./representative_strategies).

## Results

Results can be generated with:

```bash
bash scripts/analyse.sh
```

The default output directory is ./results. You can configure this and other parameters with optional arguments. The most important would be `-n <int>` to set the number of processes.

## Contents

| Path | Description |
|---|---|
| `src/emergent_llm/` | Games, strategy generation, tournaments, cultural evolution |
| `src/emergent_llm/generation/prompts.py` | All prompts used for strategy generation |
| `strategies/<game>/<model>_descriptions.py` | Natural-language strategy descriptions (LLM output) |
| `strategies/<game>/<model>.py` | Python implementations (LLM output) |
| `representative_strategies/` | Strategies closest to each PCA centroid, for quick inspection |
| `scripts/` | Experiment and plotting scripts |
