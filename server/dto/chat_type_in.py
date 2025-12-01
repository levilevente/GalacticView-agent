from pydantic import BaseModel

from datetime import datetime

from pydantic import Field

class ChatTypeIn(BaseModel):
    """Data transfer object for chat type input."""
    question: str = Field(..., min_length=1, max_length=512)
    datetime: datetime