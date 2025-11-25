# Social Dilemma Experiments

A benchmark for assessing LLM behaviour in multi-player social dilemma games, investigating whether large language models exhibit differential capabilities with exploitative vs collective strategies.

This repository is under active development, and aims to extend the paper ["Will Systems of LLM Agents Lead to Cooperation: An Investigation into a Social Dilemma"](https://ifaamas.csc.liv.ac.uk/Proceedings/aamas2025/pdfs/p2786.pdf) from my earlier repo [evo_llm](github.com/willis-richard/evo_llm). to multi-player games.

## Overview

This project investigates the emergent behaviour of LLM-driven autonomous agents in multi-agent social dilemmas. The key research question is whether LLMs are more successful with exploitative strategies compared to collective, cooperative approaches, and what this means for potential negative social outcomes.

### Key Features

- **Strategy Generation**: LLMs generate strategies in natural language, then implement them as Python functions
- **Multiple Games**: Support for Public Goods Game (PGG), with plans for Collective Risk Dilemma (CRD) and Common Pool Resource (CPR) games
- **Fair Tournaments**: All players participate in equal numbers of games via random permutation
- **Comprehensive Logging**: Detailed game histories and strategy performance metrics
- **Attitude-Based Analysis**: Compare cooperative vs. aggressive strategy performance
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

3. Update PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## Results

The generated strategies are in [strategies](./strategies). To generate new ones use:

```bash
python3 src/emergent_llm/generation/create_strategies.py --llm_provider <provider> --model_name <model_name> --n 16 --game <game>
```

Results can be generated with:

```bash
python scripts/run_tournament.py --strategies strategies/<game>/e<provider>_<model>.py --game <game>  --matches 200 --group-sizes 4 16 64 --verbose
```

The output directory is ./results.
