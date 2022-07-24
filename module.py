from traceback import StackSummary
from unicodedata import name
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    img: str = Field(...)
    summary: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Harry Potter and the Order of the Phoenix",
                "img": "https://bit.ly/2IcnSwz",
                "summary": "..."
            }
        }


class MovieUpdate(BaseModel):
    name: Optional[str]
    img: Optional[str]
    summary: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Harry Potter and the Order of the Phoenix",
                "img": "https://bit.ly/2IcnSwz",
                "summary":"Harry Potter and Dumbledore's warning about the return of
Lord Voldemort is not heeded by the wizard authorities who, in turn, look to
undermine Dumbledore's authority at Hogwarts and discredit Harry"
            }
        }