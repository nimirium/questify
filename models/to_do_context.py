from typing import Optional

from pydantic import BaseModel


class ToDoContext(BaseModel):
    title: Optional[str]
    time: str
