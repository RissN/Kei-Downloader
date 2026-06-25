"""YouTube downloader using yt-dlp."""

import asyncio
import glob
import os
import shutil
from pathlib import Path
from typing import Callable, List, Optional

import yt_dlp

from schemas import Format, InfoResponse

DOWNLOAD_DIR = Path(__file__).parent.parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)


def find_ffmpeg() -> Optional[str]:
    """Cari ffmpeg di PATH, lalu di lokasi umum Windows. Return directory path atau None."""
    # 1. Cek PATH dulu
    path_result = shutil.which("ffmpeg")
    if path_result:
        return str(Path(path_result).parent)

    # 2. Scan lokasi umum di Windows
    candidates: list[str] = []

    # WinGet — Links shortcut folder
    candidates.append(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links"))

    # WinGet — Packages (deep nested: Gyan.FFmpeg_.../ffmpeg-.../bin/)
    winget_packages = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages")
    if os.path.isdir(winget_packages):
        for p in glob.glob(os.path.join(winget_packages, "**", "ffmpeg.exe"), recursive=True):
            candidates.append(str(Path(p).parent))

    # Scoop, Chocolatey
    candidates.append(os.path.expandvars(r"%USERPROFILE%\scoop\shims"))
    candidates.append(os.path.expandvars(r"%ProgramData%\chocolatey\bin"))

    # Program Files (rekursif: */bin/, */ffmpeg.exe)
    for prog_dir in [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
    ]:
        if os.path.isdir(prog_dir):
            for pattern in [
                os.path.join(prog_dir, "*", "bin", "ffmpeg.exe"),
                os.path.join(prog_dir, "*", "ffmpeg.exe"),
                os.path.join(prog_dir, "ffmpeg", "**", "ffmpeg.exe"),
            ]:
                candidates.extend(
                    str(Path(p).parent) for p in glob.glob(pattern, recursive=True)
                )

    for candidate_dir in candidates:
        if os.path.isfile(os.path.join(candidate_dir, "ffmpeg.exe")):
            return candidate_dir

    return None


# Deteksi ffmpeg saat module load
FFMPEG_LOCATION: Optional[str] = find_ffmpeg()

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
        """Extract video info dan return format yang tersedia. Handle playlist jika ada."""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": "in_playlist",
        }

        loop = asyncio.get_event_loop()

        def _extract() -> dict:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        info = await loop.run_in_executor(None, _extract)

        title: str = info.get("title", "Unknown")

        # Jika url adalah playlist, kembalikan daftar video
        if "entries" in info:
            items = []
            for entry in info["entries"]:
                if not entry:
                    continue
                # yt-dlp flat extract might put url or id
                entry_url = entry.get("url") or (f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get("id") else "")
                
                # thumbnail fallback
                thumb = entry.get("thumbnail")
                if not thumb and entry.get("thumbnails"):
                    thumb = entry["thumbnails"][0].get("url")

                items.append(
                    {
                        "title": entry.get("title", "Unknown"),
                        "url": entry_url,
                        "duration": entry.get("duration"),
                        "thumbnail": thumb,
                    }
                )
            
            return InfoResponse(
                title=title,
                is_playlist=True,
                playlist_items=items
            )

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
        include_subtitles: bool = False,
    ) -> str:
        """Download video/audio dan return filepath."""
        opts = self._build_ydl_opts(format_id, task_id, progress_callback, include_subtitles)

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
        include_subtitles: bool = False,
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

        if FFMPEG_LOCATION:
            opts["ffmpeg_location"] = FFMPEG_LOCATION

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

            if include_subtitles:
                opts["writesubtitles"] = True
                opts["subtitleslangs"] = ["id", "en"]
                opts["embedsubtitles"] = True
                opts["compat_opts"] = set() # Avoid subtitle format issues
                opts["postprocessors"] = opts.get("postprocessors", []) + [
                    {
                        "key": "FFmpegEmbedSubtitle",
                        "already_have_subtitle": False,
                    }
                ]

        return opts
