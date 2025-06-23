from pydantic import BaseModel
from typing import Optional


class TrackRequest(BaseModel):
    track_name: str


class DownloadResponse(BaseModel):
    title: str
    filename: str
    filepath: str
    duration: Optional[int] = None
    uploader: Optional[str] = None
