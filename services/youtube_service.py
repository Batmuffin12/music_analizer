from pathlib import Path
import yt_dlp
import os


class YoutubeDownloader:

    def __init__(self, ffmpeg_path: str = r"C:\ffmpeg\bin"):
        self.ffmpeg_path = ffmpeg_path

    @staticmethod
    def download_mp3(track_name: str, output_dir: str = "downloads"):
        """Download YouTube audio as mono MP3"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        options = {
            "format": "bestaudio/best",
            "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "postprocessor_args": ["-ac", "1"],  # mono conversion
            "default_search": "ytsearch1:",
            "noplaylist": True,
            "ffmpeg_location": r"C:\ffmpeg\bin",
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(track_name, download=True)
            video_info = info["entries"][0] if "entries" in info else info

            title = video_info.get("title", "Unknown")
            filename = f"{title}.mp3"
            filepath = os.path.join(output_dir, filename)

            return {
                "title": title,
                "filename": filename,
                "filepath": filepath,
                "duration": video_info.get("duration"),
                "uploader": video_info.get("uploader"),
            }
