from modules.logger import get_logger
from modules.config import CHAIN_LLM,OUTPUT_FILENAME
from modules.audio_process import remove_non_ascii

logger = get_logger("model-process logger")


def policy_assistant(transcript):

    try:
        
        if not transcript:
            raise ValueError("Transcript is not found")
        
        process_transcript = remove_non_ascii(transcript)
        logger.info("transcript formatted")
        
        result = CHAIN_LLM.invoke(input={"context": process_transcript})
        if result:
            logger.info("results is fetched")    
            logger.info("Started deployment")
            
            with open(OUTPUT_FILENAME, "w") as file:
                file.write(result)
                   
            return result, OUTPUT_FILENAME
        else:
            raise ValueError("Result is created unsucessfull")

    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error in policy assistant: {e}")
        return None
