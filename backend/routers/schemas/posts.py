# router/schemas/posts.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    author_id: int
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class PostPublishRequest(BaseModel):
    author_id: int


class PostArchiveRequest(BaseModel):
    author_id: int


class PostResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    slug: str
    status: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
