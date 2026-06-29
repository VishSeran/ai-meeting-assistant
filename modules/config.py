from transformers import pipeline

STT_MODEL_NAME = "openai/whisper-tiny.en"
LLM_MODEL = "meta-llama/llama-3-2-11b-vision-instruct"

STT_PIPE = pipeline(
    task="automatic-speech-recognition", model=STT_MODEL_NAME, chunk_length_s=30
)
