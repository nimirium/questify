from typing import Optional

from pydantic import BaseModel


class ToDoContext(BaseModel):
    toDoListTitle: Optional[str]
    currentTime: str
