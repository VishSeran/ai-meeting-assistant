from modules.logger import get_logger
from modules.config import LLM_MODEL, CHAT_LLM, CHAIN_LLM
from modules.audio_process import remove_non_ascii
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = get_logger("model-process logger")


def policy_assistant(transcript):

    try:
        

        if not transcript:
            raise ValueError("Transcript is not found")
        
        process_transcript = remove_non_ascii(transcript)
        result = CHAIN_LLM.invoke(process_transcript)
        
        return result

    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error in policy assistant: {e}")
        return None
