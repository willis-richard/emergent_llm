"""Generate prompt-word variants without modifying the core generation pipeline.

This wrapper reuses ``create_strategies.py`` but swaps in a runtime-only
prompt builder that keeps the original public goods prompt structure while
changing the attitude word.
"""
import argparse
import os
from contextlib import contextmanager
from pathlib import Path

import emergent_llm.generation.create_strategies as cs
from emergent_llm.common import Attitude
from emergent_llm.generation.prompts import format_game_description


WORD_TO_ATTITUDE: dict[str, Attitude] = {
    "collective": Attitude.COLLECTIVE,
    "prosocial": Attitude.COLLECTIVE,
    "communal": Attitude.COLLECTIVE,
    "exploitative": Attitude.EXPLOITATIVE,
    "aggressive": Attitude.EXPLOITATIVE,
    "opportunistic": Attitude.EXPLOITATIVE,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate prompt-word strategy variants using the old prompt template."
    )
    parser.add_argument("--llm_provider",
                        choices=["openai", "anthropic", "ollama", "google",
                                 "openrouter"],
                        required=True)
    parser.add_argument("--model_name", required=True)
    parser.add_argument("--prompt_word",
                        choices=sorted(WORD_TO_ATTITUDE),
                        required=True,
                        help="Word substituted into the old prompt template.")
    parser.add_argument("--game_name",
                        choices=["public_goods", "collective_risk",
                                 "common_pool"],
                        default="public_goods")
    parser.add_argument("--strategies_dir", default="strategies")
    parser.add_argument(
        "--output_name",
        default=None,
        help=("Optional file stem for outputs. Defaults to "
              "<safe-model-name>__<prompt-word>."))

    subparsers = parser.add_subparsers(dest="phase", required=True)
    desc_parser = subparsers.add_parser("descriptions")
    desc_parser.add_argument("--n",
                             type=int,
                             required=True,
                             help="Number of strategies to generate.")

    impl_parser = subparsers.add_parser("implementations")
    impl_parser.add_argument("--max_retries", type=int, default=3)

    return parser.parse_args()


def create_old_prompt_with_word(prompt_word: str, game_name: str) -> str:
    state = ", state" if game_name == "common_pool" else ""
    return f"""{format_game_description(game_name)}

Standard game theory assumptions hold:
- Perfect information: All players can observe all other players' actions and payoffs from previous rounds
- Common knowledge: All players know the game rules, parameters and payoff structure
- Simultaneous actions: This is a normal-form game
- Repeated interaction: The game is played for multiple rounds (r > 1)
- No communication: Players cannot communicate, signal or otherwise share information

Design a {prompt_word} strategy for this game that only depends on the game parameters{state} and history. Your strategy should be adaptive and robust to a wide range of opponent behaviours.

1. Specify decision rules - When exactly do you cooperate vs defect?
2. Handle edge cases - What do you do in the first round, last round, etc.?
3. Be {prompt_word} - Clearly align with the {prompt_word} mindset

Your strategy will play in a tournament against independent strategies developed by other AI systems. You cannot rely on others sharing norms, nor can you assume any specific coordination mechanisms such as cooperation schedules or predetermined patterns.

You only need to describe the strategy in natural language, including pseudocode if helpful. Later, the strategy will be implemented as an algorithm."""


@contextmanager
def patched_prompt_builder(prompt_word: str):
    original = cs.create_strategy_user_prompt

    def _patched(attitude: Attitude, game_name: str) -> str:
        del attitude
        return create_old_prompt_with_word(prompt_word, game_name)

    cs.create_strategy_user_prompt = _patched
    try:
        yield
    finally:
        cs.create_strategy_user_prompt = original


def create_client(llm_provider: str):
    if llm_provider == "openai":
        return cs.openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    if llm_provider == "anthropic":
        return cs.anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    if llm_provider == "ollama":
        return cs.ollama.Client(host=os.environ["OLLAMA_HOST"])
    if llm_provider == "openrouter":
        return cs.openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
    if llm_provider == "google":
        return cs.genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    raise ValueError(f"Unknown client {llm_provider}")


def resolve_output_name(model_name: str, prompt_word: str,
                        output_name: str | None) -> str:
    if output_name is not None:
        return cs.make_safe(output_name.replace("/", "-"))
    return f"{cs.make_safe(model_name.replace('/', '-'))}__{prompt_word}"


def main():
    args = parse_args()
    prompt_attitude = WORD_TO_ATTITUDE[args.prompt_word]

    strategies_dir = Path(args.strategies_dir) / args.game_name
    strategies_dir.mkdir(parents=True, exist_ok=True)
    log_dir = strategies_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    output_stem = resolve_output_name(args.model_name, args.prompt_word,
                                      args.output_name)
    description_file = strategies_dir / f"{output_stem}_descriptions.py"
    strategy_file = strategies_dir / f"{output_stem}.py"
    log_file = log_dir / f"{output_stem}_{args.phase}.log"

    logger = cs.setup_logging(log_file)
    logger.info("Prompt-word variant generation started")
    logger.info("Checkpoint model: %s", args.model_name)
    logger.info("Output stem: %s", output_stem)
    logger.info("Prompt word: %s", args.prompt_word)
    logger.info("Canonical attitude: %s", prompt_attitude)
    logger.info("Game: %s", args.game_name)

    config = cs.LLMConfig(create_client(args.llm_provider), args.model_name)

    with patched_prompt_builder(args.prompt_word):
        if args.phase == "descriptions":
            cs.generate_descriptions(config, args.game_name, [prompt_attitude],
                                     args.n, description_file, logger)
        else:
            cs.generate_implementations(config, args.game_name,
                                        description_file, strategy_file,
                                        logger, args.max_retries)

    logger.info("Prompt-word variant generation complete")


if __name__ == "__main__":
    main()
