"""Pydantic models for request/response schemas."""

from typing import List, Literal, Optional

from pydantic import BaseModel


class InfoRequest(BaseModel):
    url: str


class Format(BaseModel):
    format_id: str
    ext: str
    resolution: str
    filesize_approx: Optional[int] = None
    quality_label: str
    type: Literal["video", "audio"]


class InfoResponse(BaseModel):
    title: str
    thumbnail: str
    duration: int
    formats: List[Format]


class DownloadRequest(BaseModel):
    url: str
    format_id: str
    task_id: str


class DownloadStatus(BaseModel):
    task_id: str
    status: Literal["pending", "downloading", "done", "error"]
    progress: float = 0.0
    filename: Optional[str] = None
    error_msg: Optional[str] = None
