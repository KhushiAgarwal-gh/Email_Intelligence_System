from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["Work", "Personal", "Finance", "Promotions", "Support", "Other"]
Priority = Literal["High", "Medium", "Low"]
ProcessingStatus = Literal["pending", "processed", "failed"]
AnalysisSource = Literal["none", "llm", "fallback", "manual"]


class EmailCreate(BaseModel):
    sender: str = Field(..., min_length=1, max_length=255, examples=["alice@example.com"])
    subject: str = Field(..., min_length=1, max_length=500, examples=["Meeting tomorrow"])
    body: str = Field(..., min_length=1, examples=["Can we move the standup to 10am?"])
    category: Category | None = None
    priority: Priority | None = None
    summary: str | None = Field(default=None, max_length=2000)
    analyze: bool = True


class EmailUpdate(BaseModel):
    sender: str | None = Field(default=None, min_length=1, max_length=255)
    subject: str | None = Field(default=None, min_length=1, max_length=500)
    body: str | None = Field(default=None, min_length=1)
    category: Category | None = None
    priority: Priority | None = None
    summary: str | None = Field(default=None, max_length=2000)
    processing_status: ProcessingStatus | None = None


class EmailRead(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    category: str | None
    priority: str | None
    summary: str | None
    processing_status: str
    analysis_source: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EmailListResponse(BaseModel):
    items: list[EmailRead]
    total: int
    page: int
    page_size: int


class StatsResponse(BaseModel):
    total: int
    high_priority: int
    processed: int
    pending: int
    by_category: dict[str, int]
    by_priority: dict[str, int]
    analysis_sources: dict[str, int]
