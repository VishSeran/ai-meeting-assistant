from transformers import pipeline
import torch
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer

STT_MODEL_NAME = "openai/whisper-tiny.en"
LLM_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

STT_PIPE = pipeline(
    task="automatic-speech-recognition", model=STT_MODEL_NAME, chunk_length_s=30
)

bits_and_bytes_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)


LLM_MODEL = AutoModelForCausalLM.from_pretrained(LLM_MODEL_ID, 
                                                quantization_config = bits_and_bytes_config,
                                                device_map = "auto")

tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)


hf_pipe = pipeline(
    model_id=LLM_MODEL,
    task="text-generation",
    tokenizer=tokenizer,
    max_new_tokens = 256,
    temperature=0.7
)

LLM = HuggingFacePipeline(pipeline=hf_pipe)
CHAT_LLM = ChatHuggingFace(llm=LLM)