"""Pydantic models for request/response schemas."""

import re
from typing import List, Literal, Optional

from pydantic import BaseModel, field_validator


# --- Validation patterns ---
_YT_URL_RE = re.compile(
    r"^https?://(www\.)?(youtube\.com|youtu\.be|m\.youtube\.com)/"
)
_VIDEO_FORMAT_RE = re.compile(r"^\d{2,5}$")
_AUDIO_FORMAT_RE = re.compile(r"^bestaudio-(mp3|opus)-\d{1,3}$")
_TASK_ID_RE = re.compile(r"^[a-f0-9\-]{36}$")


class InfoRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, v: str) -> str:
        if not _YT_URL_RE.match(v):
            raise ValueError("Only YouTube URLs are allowed")
        return v


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


def is_valid_task_id(task_id: str) -> bool:
    """Check if task_id is a valid UUID format."""
    return bool(_TASK_ID_RE.match(task_id))


def is_valid_format_id(format_id: str) -> bool:
    """Check if format_id matches expected video or audio pattern."""
    return bool(_VIDEO_FORMAT_RE.match(format_id) or _AUDIO_FORMAT_RE.match(format_id))


def is_valid_youtube_url(url: str) -> bool:
    """Check if URL matches allowed YouTube domains."""
    return bool(_YT_URL_RE.match(url))
