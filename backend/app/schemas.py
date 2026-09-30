from typing import Literal

from pydantic import BaseModel, Field


class HistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=8000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: list[HistoryItem] = Field(default_factory=list, max_length=50)


class ChatResponse(BaseModel):
    response: str