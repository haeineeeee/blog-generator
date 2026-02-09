from typing import Optional

from pydantic import BaseModel


# Request models

class OutlineRequest(BaseModel):
    keyword: str
    tone: Optional[str] = None
    language: str = "ko"


class DraftRequest(BaseModel):
    keyword: str
    outline: str
    tone: Optional[str] = None


class ReviewRequest(BaseModel):
    keyword: str
    draft: str


class FullGenerateRequest(BaseModel):
    keyword: str
    tone: Optional[str] = None
    language: str = "ko"


class WordPressPublishRequest(BaseModel):
    title: str
    content: str
    status: str = "draft"


class MarkdownSaveRequest(BaseModel):
    title: str
    content: str
    filename: Optional[str] = None


# Response models

class OutlineResponse(BaseModel):
    keyword: str
    outline: str


class DraftResponse(BaseModel):
    keyword: str
    outline: str
    draft: str


class ReviewResponse(BaseModel):
    keyword: str
    draft: str
    reviewed: str
    feedback: str


class FullGenerateResponse(BaseModel):
    keyword: str
    outline: str
    draft: str
    reviewed: str
    feedback: str


class PublishResponse(BaseModel):
    success: bool
    message: str
    url: Optional[str] = None
