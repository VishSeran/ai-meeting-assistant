from transformers import pipeline
import torch
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage

STT_MODEL_NAME = "openai/whisper-tiny.en"
LLM_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
OUTPUT_FILENAME = "meeting_minutes_and_tasks.txt"

device = 0 if torch.cuda.is_available() else -1

STT_PIPE = pipeline(
    task="automatic-speech-recognition",
    model=STT_MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

bits_and_bytes_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)


LLM = HuggingFacePipeline.from_model_id(
    model_id=LLM_MODEL_ID,
    task="text-generation",
    model_kwargs={"quantization_config": bits_and_bytes_config, "device_map": "auto"},
    pipeline_kwargs={
        "temperature": 0.2,
        "top_p": 0.9,
        "do_sample": True,
        "repetition_penalty": 1.15,
        "return_full_text": False
    },
)

CHAT_LLM = ChatHuggingFace(llm=LLM)


system_prompt = """
You are a financial meeting extraction system.

CRITICAL RULES:
- Follow format EXACTLY
- Do NOT repeat any field or label
- Do NOT create empty lines or blank values
- If information is missing, write: Not specified
- Output must be clean and deterministic
- No extra text allowed outside the format
- Each bullet must appear only once

OUTPUT FORMAT:

Meeting Summary:
- Key discussion points: single consolidated bullet list
- Financial metrics mentioned: only numeric values + metric names
- Decisions made: only explicit decisions or "Not specified"

Action Items:
Each item must be in this format:
Responsible person - Task - Deadline (or Not specified)

Rules:
- One action per line
- No repeated “Responsible person” labels
- Do not split fields across lines

Modified Terms:
Original → Expanded form
(If none, write: Not specified)
"""

user_prompt = """
Context:
{context}

"""


PROMPT = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", user_prompt)]
)

def clean_output(text):
    lines = text.split("\n")
    cleaned = []
    seen = set()

    for line in lines:
        if line.strip() and line not in seen:
            cleaned.append(line)
            seen.add(line)

    return "\n".join(cleaned)

CHAIN_LLM = PROMPT | CHAT_LLM | StrOutputParser() | clean_output
