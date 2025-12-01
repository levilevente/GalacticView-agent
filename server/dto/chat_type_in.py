from pydantic import BaseModel

class ChatTypeIn(BaseModel):
    """Data transfer object for chat type input."""
    question: str
    datetime: str