from transformers import pipeline
import torch
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

STT_MODEL_NAME = "openai/whisper-tiny.en"
LLM_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
OUTPUT_FILENAME = "meeting_minutes_and_tasks.txt"

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


system_prompt = """You are an intelligent assistant specializing in financial products;
    your task is to process transcripts of earnings calls, ensuring that all references to
     financial products and common financial terms are in the correct format. For each
     financial product or common term that is typically abbreviated as an acronym, the full term 
    should be spelled out followed by the acronym in parentheses. For example, '401k' should be
     transformed to '401(k) retirement savings plan', 'HSA' should be transformed to 'Health Savings Account (HSA)' , 'ROA' should be transformed to 'Return on Assets (ROA)', 'VaR' should be transformed to 'Value at Risk (VaR)', and 'PB' should be transformed to 'Price to Book (PB) ratio'. Similarly, transform spoken numbers representing financial products into their numeric representations, followed by the full name of the product in parentheses. For instance, 'five two nine' to '529 (Education Savings Plan)' and 'four zero one k' to '401(k) (Retirement Savings Plan)'. However, be aware that some acronyms can have different meanings based on the context (e.g., 'LTV' can stand for 'Loan to Value' or 'Lifetime Value'). You will need to discern from the context which term is being referred to  and apply the appropriate transformation. In cases where numerical figures or metrics are spelled out but do not represent specific financial products (like 'twenty three percent'), these should be left as is. Your role is to analyze and adjust financial product terminology in the text. Once you've done that, produce the adjusted transcript and a list of the words you've changed"""


template = system_prompt + """
            Generate meeting minutes and a list of tasks based on the provided context.

            Context:
            {context}

            Meeting Minutes:
            - Key points discussed
            - Decisions made

            Task List:
            - Actionable items with assignees and deadlines
            """
            
PROMPT = PromptTemplate(
    template=template,
    input_variables=['context'])
        
CHAIN_LLM = PROMPT | CHAT_LLM | StrOutputParser()