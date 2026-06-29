from modules.audio_process import audio_to_text
from modules.logger import get_logger
from modules.model_process import policy_assistant

logger = get_logger("app-logger")

def speech_to_text(audio_file_path):
    
    try:
        text = audio_to_text(audio_file_path)
        result, output_file = policy_assistant(text)
        
        return result, output_file
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error in policy assistant: {e}")
        return None