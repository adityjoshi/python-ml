from pydantic import BaseModel, ConfigDict, Field
from typing import List

class NoteBookCreate(BaseModel):
    title: str = Field(...,min_length=1)
    author: str = Field(...,min_length=1)

class NoteBookOut(BaseModel):
    id: int
    title: str
    author: str
    model_config = ConfigDict(from_attributes=True)

class EntryCreate(BaseModel):
    heading: str = Field(...,min_length=1)
    mood: str = Field(...,min_length=1)
    word_count: str = Field(...,ge=1)

class EntryOut(BaseModel):
    id: int
    heading: str
    mood: str
    word_count: str

class NoteBookEntries(BaseModel):
    id: int
    title: str
    author: str
    entries: List[EntryOut]
