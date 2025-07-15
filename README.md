# Social Dilemma Experiments

A benchmark for assessing LLM behavior in social dilemma games, investigating whether large language models exhibit differential capabilities with aggressive vs. cooperative strategies.

## Overview

This project investigates the emergent behavior of LLM-driven autonomous agents in social dilemmas. The key research question is whether LLMs are more successful with exploitative strategies compared to collective, cooperative approaches, and what this means for potential negative social outcomes.

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

### Using Conda (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/willis-richard/emergent_llm.git
cd emergent_llm
```
