from enum import Enum

from pydantic import BaseModel


class MessageSenderRole(Enum):
    USER = "user"
    SYSTEM = "system"


class Message(BaseModel):
    role: MessageSenderRole
    content: str
