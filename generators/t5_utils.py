# generators/t5_utils.py
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import random
import numpy as np

MODEL_NAME = "google/flan-t5-base"
MAX_INPUT_TOKENS = 256
GLOBAL_SEED = 42


def set_seed(seed=GLOBAL_SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

set_seed()

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading T5 model:", MODEL_NAME)

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

model.to(DEVICE)
model.eval()

print("T5 loaded successfully")


def t5_generate(prompt, max_tokens=40):

    if not prompt:
        return ""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_INPUT_TOKENS
    ).to(DEVICE)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False
        )

    result = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    return result


# ---------------------------------
# PROMPT BUILDERS
# ---------------------------------
def build_short_question_prompt(context, concept=None, bloom=None):

    short_context = context[:500]

    concept_text = f"Concept: {concept}" if concept else ""

    bloom_text = (
        f"Generate a {bloom.lower()} level short answer question."
        if bloom else
        "Generate a short answer question."
    )

    return f"""
{bloom_text}

{concept_text}

Context:
{short_context}

Question:
"""
def build_mcq_prompt(context):

    return f"""
Generate a multiple choice question from the context.

Context:
{context}

Output format:
Question:
Options:
A)
B)
C)
D)
Answer:
"""


def build_true_false_prompt(context):

    return f"""
Generate a true or false question from the context.

Context:
{context}

Output:
True or False statement:
"""