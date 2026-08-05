from pydantic import BaseModel
from datetime import datetime

class NoteIn(BaseModel):
	title: str
	content: str
	completed: bool

class NoteOut(BaseModel): 
  id: int
  created_at: datetime

class NotePatch(BaseModel):
	title: str | None = None
	content: str | None = None
	completed: bool | None = None