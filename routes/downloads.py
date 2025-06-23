from fastapi import APIRouter, HTTPException

from models.schemas.download_schemas import DownloadResponse, TrackRequest
from services.youtube_service import YoutubeDownloader

router = APIRouter(
    prefix="/downloads",
    tags=["downloads"],
)


@router.post("/download", response_model=DownloadResponse)
def download_track(request: TrackRequest):
    """Download audio track from YouTube as MP3"""
    try:
        result = YoutubeDownloader.download_mp3(request.track_name)
        return DownloadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
