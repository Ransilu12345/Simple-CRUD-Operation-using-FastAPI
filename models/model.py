from pydantic import BaseModel
from typing import Optional

class BAeModels(BaseModel):
    """Pydantic model describing a chat/memory item stored in MongoDB.

    Fields:
        id: Application-level identifier for the item (separate from Mongo _id).
        name: Name of the user or item owner.
        email: Contact email associated with the item.
        message: The main message/body content.
        summary: Optional short summary of the message.
    """
    id: str
    name: str
    email: str
    message: str
    summary: Optional[str]