"""Example of reannotating the OpenHermes dataset using curator."""

import logging

from datasets import load_dataset

from bespokelabs import curator

# To see more detail about how batches are being processed
logger = logging.getLogger("bespokelabs.curator")
logger.setLevel(logging.INFO)


def convert_row(row: dict) -> dict:
    """Convert a conversation row from OpenHermes format to instruction/response format.

    Args:
        row: Dictionary containing a conversation from the OpenHermes dataset

    Returns:
        Dictionary with 'instruction' and 'original_response' fields extracted from the conversation
    """
    conversation = row["conversations"]
    instruction = next((item["value"] for item in conversation if item["from"] == "human"), None)
    response = next((item["value"] for item in conversation if item["from"] == "gpt"), None)
    return {"instruction": instruction, "original_response": response}


def prompt_func(row):
    """Extract the instruction to be used as the prompt.

    Args:
        row: Dictionary containing the instruction and original response

    Returns:
        The instruction string to be used as the prompt
    """
    return row["instruction"]


def parse_func(row, response):
    """Parse the model response into the desired output format.

    Args:
        row: Dictionary containing the original instruction and response
        response: The new response generated by the model

    Returns:
        Dictionary containing the instruction and new response
    """
    instruction = row["instruction"]
    return {"instruction": instruction, "new_response": response}


distill_prompter = curator.LLM(
    prompt_func=prompt_func, parse_func=parse_func, model_name="claude-3-5-sonnet-20241022", batch=True, backend_params={"batch_size": 100}
)

dataset = load_dataset("teknium/OpenHermes-2.5", split="train")
dataset = dataset.take(500)
dataset = dataset.map(convert_row)
dataset = dataset.select_columns(["instruction", "original_response"])
distilled_dataset = distill_prompter(dataset)
print(distilled_dataset)
print(distilled_dataset[0])
