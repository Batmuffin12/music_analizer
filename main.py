from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import os
from pathlib import Path

app = FastAPI(title="YouTube Audio Downloader", version="1.0.0")


class TrackRequest(BaseModel):
    track_name: str


class DownloadResponse(BaseModel):
    title: str
    filename: str
    filepath: str
    duration: int = None
    uploader: str = None
    view_count: int = None


def search_and_download_youtube_audio(track_name: str, output_dir: str = "downloads"):
    """
    Search for a track on YouTube and download it as MP3
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Set your specific FFmpeg path
    ffmpeg_location = r"C:\ffmpeg\bin"

    # Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "audioquality": "192",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
                "postprocessor_args": ["-ac", "1", "-af", "pan=mono|c0=0.5*c0+0.5*c1"],
            }
        ],
        "default_search": "ytsearch1:",  # Search YouTube and take first result
        "noplaylist": True,  # Only download single video
        "ffmpeg_location": ffmpeg_location,  # Explicitly set FFmpeg location
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search and download
            info = ydl.extract_info(track_name, download=True)
            if "entries" in info:
                video_info = info["entries"][0]
            else:
                video_info = info

            # Construct the expected filename
            title = video_info.get("title", "Unknown")
            filename = f"{title}.mp3"
            filepath = os.path.join(output_dir, filename)

            return {
                "title": title,
                "filename": filename,
                "filepath": filepath,
                "duration": video_info.get("duration"),
                "uploader": video_info.get("uploader"),
                "view_count": video_info.get("view_count"),
            }

    except Exception as e:
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
            try:
                fallback_opts = {
                    "format": "bestaudio",
                    "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
                    "default_search": "ytsearch1:",
                    "noplaylist": True,
                }

                with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                    info = ydl.extract_info(track_name, download=True)

                    if "entries" in info:
                        video_info = info["entries"][0]
                    else:
                        video_info = info

                    title = video_info.get("title", "Unknown")
                    ext = video_info.get("ext", "unknown")
                    filename = f"{title}.{ext}"
                    filepath = os.path.join(output_dir, filename)

                    return {
                        "title": title,
                        "filename": filename,
                        "filepath": filepath,
                        "duration": video_info.get("duration"),
                        "uploader": video_info.get("uploader"),
                        "view_count": video_info.get("view_count"),
                        "note": f"Downloaded as {ext} format (FFmpeg not available for MP3 conversion)",
                    }
            except Exception as fallback_error:
                raise Exception(f"Error downloading track: {str(fallback_error)}")
        else:
            raise Exception(f"Error downloading track: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "YouTube Audio Downloader API",
        "endpoints": {
            "/download": "POST - Download audio from YouTube",
            "/docs": "GET - API documentation",
        },
    }


@app.post("/download", response_model=DownloadResponse)
async def download_track(request: TrackRequest):
    """
    Download audio track from YouTube
    """
    try:
        result = search_and_download_youtube_audio(request.track_name)
        return DownloadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/ffmpeg-check")
async def ffmpeg_check():
    """Check if FFmpeg is available"""
    ffmpeg_path = r"C:\ffmpeg\bin"
    ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")
    ffprobe_exe = os.path.join(ffmpeg_path, "ffprobe.exe")

    return {
        "ffmpeg_path": ffmpeg_path,
        "ffmpeg_exists": os.path.exists(ffmpeg_exe),
        "ffprobe_exists": os.path.exists(ffprobe_exe),
        "ffmpeg_full_path": ffmpeg_exe,
        "ffprobe_full_path": ffprobe_exe,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
