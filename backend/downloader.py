"""YouTube downloader using yt-dlp."""

import asyncio
import os
from pathlib import Path
from typing import Callable, List

import yt_dlp

from schemas import Format, InfoResponse

DOWNLOAD_DIR = Path(__file__).parent.parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Resolusi yang di-support, urut dari tertinggi
SUPPORTED_HEIGHTS = {
    2160: "2160p",
    1440: "1440p",
    1080: "1080p",
    720: "720p",
    480: "480p",
    360: "360p",
}

AUDIO_BITRATES = [320, 192, 128]


def _snap_height(height: int) -> int | None:
    """Snap height ke resolusi terdekat jika selisih ≤ 50px."""
    best = None
    best_diff = 999
    for h in SUPPORTED_HEIGHTS:
        diff = abs(h - height)
        if diff < best_diff:
            best_diff = diff
            best = h
    return best if best_diff <= 50 else None


class YTDownloader:
    """Wrapper yt-dlp untuk extract info dan download."""

    async def get_info(self, url: str) -> InfoResponse:
        """Extract video info dan return format yang tersedia."""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        loop = asyncio.get_event_loop()

        def _extract() -> dict:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        info = await loop.run_in_executor(None, _extract)

        title: str = info.get("title", "Unknown")
        thumbnail: str = info.get("thumbnail", "")
        duration: int = info.get("duration", 0) or 0

        formats = self._parse_video_formats(info.get("formats", []))
        formats.extend(self._build_audio_formats(duration))

        return InfoResponse(
            title=title,
            thumbnail=thumbnail,
            duration=duration,
            formats=formats,
        )

    async def download(
        self,
        url: str,
        format_id: str,
        task_id: str,
        progress_callback: Callable[[float], None],
    ) -> str:
        """Download video/audio dan return filepath."""
        opts = self._build_ydl_opts(format_id, task_id, progress_callback)

        loop = asyncio.get_event_loop()
        result: dict[str, str] = {"filepath": ""}

        def _download() -> None:
            with yt_dlp.YoutubeDL(opts) as ydl:
                extracted = ydl.extract_info(url, download=True)
                if extracted:
                    downloads = extracted.get("requested_downloads", [])
                    if downloads:
                        result["filepath"] = downloads[0].get("filepath", "")
                    else:
                        fp = ydl.prepare_filename(extracted)
                        if format_id.startswith("bestaudio-"):
                            fp = os.path.splitext(fp)[0] + ".mp3"
                        result["filepath"] = fp

        await loop.run_in_executor(None, _download)
        return result["filepath"]

    def _parse_video_formats(self, raw_formats: list) -> List[Format]:
        """Filter & group video formats per resolusi unik."""
        resolution_best: dict[int, dict] = {}

        for f in raw_formats:
            height = f.get("height")
            vcodec = f.get("vcodec", "none")
            filesize = f.get("filesize") or f.get("filesize_approx")

            # Skip: no height, audio-only, or no filesize info
            if not height or vcodec in ("none", None) or not filesize:
                continue

            snapped = _snap_height(height)
            if snapped is None:
                continue

            # Keep the best (largest filesize) per resolution
            current = resolution_best.get(snapped)
            if current is None or filesize > (current.get("filesize") or 0):
                resolution_best[snapped] = {
                    **f,
                    "snapped_height": snapped,
                    "filesize": filesize,
                }

        formats: List[Format] = []
        for height in sorted(resolution_best.keys(), reverse=True):
            f = resolution_best[height]
            label = SUPPORTED_HEIGHTS[height]
            if height >= 1080:
                label += " HD"
            formats.append(
                Format(
                    format_id=f["format_id"],
                    ext="mp4",
                    resolution=SUPPORTED_HEIGHTS[height],
                    filesize_approx=f["filesize"],
                    quality_label=label,
                    type="video",
                )
            )

        return formats

    def _build_audio_formats(self, duration: int) -> List[Format]:
        """Generate audio format options (MP3 at different bitrates)."""
        formats: List[Format] = []
        for bitrate in AUDIO_BITRATES:
            estimated_size = int(bitrate * 1000 * duration / 8) if duration else None
            formats.append(
                Format(
                    format_id=f"bestaudio-{bitrate}",
                    ext="mp3",
                    resolution=f"{bitrate}kbps",
                    filesize_approx=estimated_size,
                    quality_label=f"{bitrate} kbps",
                    type="audio",
                )
            )
        return formats

    def _build_ydl_opts(
        self,
        format_id: str,
        task_id: str,
        progress_callback: Callable[[float], None],
    ) -> dict:
        """Build yt-dlp options dict."""
        is_audio = format_id.startswith("bestaudio-")

        def progress_hook(d: dict) -> None:
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)
                if total > 0:
                    pct = (downloaded / total) * 100
                    progress_callback(min(pct, 99.0))
            elif d["status"] == "finished":
                progress_callback(99.0)

        opts: dict = {
            "quiet": True,
            "no_warnings": True,
            "outtmpl": str(DOWNLOAD_DIR / f"{task_id}_%(title).80s.%(ext)s"),
            "progress_hooks": [progress_hook],
        }

        if is_audio:
            bitrate = format_id.split("-")[1]
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate,
                }
            ]
        else:
            opts["format"] = f"{format_id}+bestaudio/best"
            opts["merge_output_format"] = "mp4"

        return opts
