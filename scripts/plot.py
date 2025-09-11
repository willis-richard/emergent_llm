"""Run a fair tournament where all players play equal games."""
import logging

from emergent_llm.tournament import BatchMixtureTournamentResults

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fair_tournament.log'),
        logging.StreamHandler()
    ]
)

def main():
    paths = [
        "/home/richard/repo/emergent_llm/results/public_goods/openai_o4-mini/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/public_goods/openai_gpt-4.1-mini/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/public_goods/anthropic_claude-sonnet-4-0/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/common_pool/openai_o4-mini/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/common_pool/openai_gpt-4.1-mini/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/common_pool/anthropic_claude-sonnet-4-0/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/collective_risk/openai_o4-mini/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/collective_risk/openai_gpt-4.1-mini/batch_mixture/results.json",
        "/home/richard/repo/emergent_llm/results/collective_risk/anthropic_claude-sonnet-4-0/batch_mixture/results.json",
        ]
    for path in paths:
        check = BatchMixtureTournamentResults.load(path)
        check.create_schelling_diagrams()
        check.create_social_welfare_diagram()


if __name__ == "__main__":
    main()
