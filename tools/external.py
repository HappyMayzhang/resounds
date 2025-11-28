from ..core.predictor import predictor
from ..adapters.llm import LLM
from typing import Annotated

@predictor(LLM())
def induce_instruction(
    correct_instructions: Annotated[list[str], "correct instructions"]
) -> Annotated[str, "new instruction"]:
    """
    You are the instruction optimizer for a large-scale language model.
    I will provide you with some task instructions that I have tried
    and confirmed to be executed correctly. Your task is to summarize
    these correct instructions and propose a new one.
    """
    return ...
