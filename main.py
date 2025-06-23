from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import os
from pathlib import Path
from routes import downloads


app = FastAPI(title="YouTube MP3 Downloader", version="1.0.0")

app.include_router(downloads.router)


@app.get("/")
def root():
    return {
        "message": "YouTube MP3 Downloader API",
        "endpoints": {
            "/downloads/": "POST - Download MP3 from YouTube",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
