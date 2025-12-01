from langchain_core.tools import tool
from ddgs import DDGS

from loguru import logger

@tool
def search_internet_for_text(query: str) -> str:
    """Searches the internet for real-time information."""

    logger.info(f"Searching text for: {query}")
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            if not results:
                return "No text results found."
            summary = " ".join([result.get("body", "") for result in results])
            return summary
    except Exception as e:
        logger.error(f"Error searching for text: {e}")
        return "Error searching for text. Please try again."


@tool
def search_internet_for_images(query: str) -> list[dict[str, str]]:
    """Searches the internet for images. Returns a list of image URLs."""

    logger.info(f"Searching images for: {query}")
    try:
        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=4)
        if not results:
            return []
        return results
    except Exception as e:
        logger.error(f"Error searching for images: {e}")
        return []