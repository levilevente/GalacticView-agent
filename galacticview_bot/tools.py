from typing import Any, Dict, List

from langchain_core.tools import tool
from ddgs import DDGS


@tool
def search_internet_for_text(query: str) -> List[Dict[str, Any]]:
    """Searches the internet for real-time information and returns a list of
    result dictionaries. Always returns a list (empty on no results/error).
    """
    print(f"  🔎 Searching text for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return []
        # Ensure each result is a dict
        normalized: List[Dict[str, Any]] = []
        for r in results:
            if isinstance(r, dict):
                normalized.append(r)
            else:
                # best-effort conversion
                normalized.append({"text": str(r)})
        return normalized
    except Exception as e:
        print(f"[DEBUG] Error detail: {e}")
        return []


@tool
def search_internet_for_images(query: str) -> List[Dict[str, Any]]:
    """Searches the internet for images and returns a list of image result
    dictionaries. Always returns a list (empty on no results/error).
    """
    print(f"  📸 Searching images for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=4))
        if not results:
            return []
        normalized: List[Dict[str, Any]] = []
        for r in results:
            if isinstance(r, dict):
                normalized.append(r)
            else:
                normalized.append({"url": str(r)})
        return normalized
    except Exception as e:
        print(f"[DEBUG] Error detail: {e}")
        return []
