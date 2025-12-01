import os
import sys
from typing import Any
from dotenv import load_dotenv
from loguru import logger

def setup_logging() -> Any:
    """
    Configures the global Loguru logger based on environment variables.
    """
    load_dotenv()
    
    log_level = os.getenv("LOGGING_LEVEL", "INFO").upper()

    logger.remove(0) 

    logger.add(
      level=log_level,
      sink=sys.stdout, 
    )
    
    return logger

setup_logging()