from modules.logger import get_logger
import requests

logger = get_logger("audio-process-logger")

def download_audio (url, filename):
    
    try:
        
        if not url:
            raise ValueError("Audio URL cannot be empty or none")
        
        if not filename:
            raise ValueError("audio file name is empty or none")
        
        response = requests.get(url=url)
        
        if response.status_code == 200:
            logger.info("Response fetched from URL")
            with open(filename, "wb") as file:
                file.write(response.content)
                logger.info("Audio file has created")
                return file
        else:
            raise ValueError(f"Error in downloading audio: {response.status_code}")
        
    except Exception as e:
        logger.error(f"Error in download audio: {e}")
        return None
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

