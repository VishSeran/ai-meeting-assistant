import logging

def get_logger(name:str):
    
    try:
        if not name:
            raise ValueError("logger name cannot be empty or none")
        
        logging.basicConfig(
           level= logging.INFO,
           format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        logger = logging.getLogger(name)
        return logger
    except Exception as e:
        print(f"Error in {name} logger: {e}")
        
    except ValueError as e:
        print(f"Value error: {e}")