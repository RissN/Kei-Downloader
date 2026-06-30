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


class PlaylistItem(BaseModel):
    title: str
    url: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None

class InfoResponse(BaseModel):
    title: str
    thumbnail: Optional[str] = ""
    duration: Optional[int] = 0
    formats: List[Format] = []
    is_playlist: bool = False
    playlist_items: List[PlaylistItem] = []


class DownloadRequest(BaseModel):
    url: str
    format_id: str
    task_id: str


class DownloadStatus(BaseModel):
    task_id: str
    status: Literal["pending", "downloading", "streaming", "done", "error"]
    progress: float = 0.0
    filename: Optional[str] = None
    error_msg: Optional[str] = None
