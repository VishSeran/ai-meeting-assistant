from transformers import pipeline

STT_MODEL_NAME = "openai/whisper-tiny.en"

STT_PIPE = pipeline(
    task="automatic-speech-recognition", model=STT_MODEL_NAME, chunk_length_s=30
)
