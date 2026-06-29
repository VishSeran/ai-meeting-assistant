from modules.logger import get_logger
from modules.config import LLM_MODEL

logger = get_logger("model-process logger")

def policy_assistant(transcript):
    
    try:
        
        if not transcript:
            raise ValueError("Transcript is not found")
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error in policy assistant: {e}")
        return None

