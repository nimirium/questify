from typing import Optional, List

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    text: str
    tags: Optional[List[str]]
