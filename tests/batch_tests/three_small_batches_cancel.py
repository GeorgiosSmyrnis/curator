from bespokelabs.curator import Prompter
from datasets import Dataset
import logging

logger = logging.getLogger("bespokelabs.curator")
logger.setLevel(logging.DEBUG)

dataset = Dataset.from_dict({"prompt": ["just say 'hi'"] * 3})

prompter = Prompter(
    prompt_func=lambda row: row["prompt"],
    model_name="gpt-4o-mini",
    response_format=None,
    batch=True,
    batch_size=1,
    batch_check_interval=10,
    batch_cancel=True,
)

dataset = prompter(dataset)
print(dataset.to_pandas())
