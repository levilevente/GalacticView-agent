import os
import sys
from dotenv import load_dotenv
from loguru import logger

def setup_logging() -> None:
    """
    Configures the global Loguru logger based on environment variables.
    """
    load_dotenv()
    
    log_level = os.getenv("LOGGING_LEVEL", "INFO").upper()

    try:
        logger.remove()
    except ValueError:
        pass
      
    logger.add(
      level=log_level,
      sink=sys.stdout, 
      format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

setup_logging()