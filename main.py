"""FastAPI application — YouTube Downloader backend."""

import asyncio
import json
import logging
import os
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple
from urllib.parse import quote
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from downloader import YTDownloader
from schemas import DownloadStatus, InfoRequest, is_valid_task_id

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YT Downloader API")

# --- CORS ---
allowed_origins_str = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000,http://127.0.0.1:8000")
origins = [o.strip() for o in allowed_origins_str.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length"],
)

# --- Security headers middleware (#7) ---
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# --- Rate limiter (#5) ---
_RATE_LIMIT_WINDOW = 60  # seconds
_RATE_LIMIT_MAX = 30  # requests per window
_rate_limit_store: Dict[str, list] = defaultdict(list)


def _check_rate_limit(ip: str) -> bool:
    """Return True if request is allowed, False if rate limited."""
    now = time.time()
    _rate_limit_store[ip] = [t for t in _rate_limit_store[ip] if now - t < _RATE_LIMIT_WINDOW]
    if len(_rate_limit_store[ip]) >= _RATE_LIMIT_MAX:
        return False
    _rate_limit_store[ip].append(now)
    return True


# --- Global state ---
task_progress: Dict[str, Tuple[DownloadStatus, float]] = {}  # (status, timestamp)
downloader = YTDownloader()

DOWNLOAD_DIR = Path(os.environ.get("DOWNLOAD_DIR", str(Path(__file__).parent / "downloads")))
DOWNLOAD_DIR.mkdir(exist_ok=True)

MAX_TASK_AGE = 3600  # 1 hour TTL for task entries
SSE_MAX_ITERATIONS = 600  # 5 minutes at 0.5s intervals


def _cleanup_old_tasks() -> None:
    """Remove task entries older than MAX_TASK_AGE."""
    now = time.time()
    expired = [k for k, (_, ts) in task_progress.items() if now - ts > MAX_TASK_AGE]
    for k in expired:
        del task_progress[k]


# --- Startup ---
@app.on_event("startup")
async def startup_check() -> None:
    from downloader import FFMPEG_LOCATION

    if FFMPEG_LOCATION:
        logger.info("ffmpeg found: %s", FFMPEG_LOCATION)
    else:
        logger.warning(
            "ffmpeg not found. Audio conversion and video merge will fail."
        )

    # Cleanup orphaned download files (#10)
    for f in DOWNLOAD_DIR.iterdir():
        if f.is_file():
            age = time.time() - f.stat().st_mtime
            if age > MAX_TASK_AGE:
                try:
                    f.unlink()
                    logger.info("Cleaned up orphaned file: %s", f.name)
                except OSError:
                    pass

    # Cleanup stale task entries
    _cleanup_old_tasks()


# --- Endpoints ---
@app.get("/api/health")
async def health() -> dict:
    import yt_dlp

    return {"status": "ok", "yt_dlp_version": yt_dlp.version.__version__}


def sanitize_error_message(msg: str) -> str:
    msg_lower = msg.lower()
    if "is not a valid url" in msg_lower or "unsupported url" in msg_lower:
        return "YouTube URL is invalid or unsupported. Please check your link."
    if "private video" in msg_lower:
        return "This video is private and cannot be accessed."
    if "not available" in msg_lower or "unavailable" in msg_lower:
        return "Video is unavailable or restricted in your region."
    if "copyright" in msg_lower:
        return "This video cannot be downloaded due to a copyright claim."
    if "sign in to confirm your age" in msg_lower or "age-gated" in msg_lower:
        return "This video is age-restricted by YouTube."
    if "file not found" in msg_lower:
        return "Failed to process the downloaded file. Please try again."
    if "only youtube urls are allowed" in msg_lower:
        return "Only YouTube URLs are allowed."
    if "invalid format" in msg_lower:
        return "Invalid format. Please choose a different format."
    if "file is too large" in msg_lower or "max_filesize" in msg_lower:
        return f"File is too large (max {os.environ.get('MAX_FILESIZE_MB', '5000')} MB)."
    return "An error occurred while processing the video. Please try again or choose a different format."


@app.post("/api/info")
async def get_info(req: InfoRequest, request: Request) -> dict:
    # Rate limiting
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please try again in a moment.")

    try:
        info = await downloader.get_info(req.url)
        return info.model_dump()
    except Exception as e:
        logger.exception("Error fetching video info")
        clean_msg = sanitize_error_message(str(e))
        if "invalid" in clean_msg.lower() or "only" in clean_msg.lower():
            raise HTTPException(status_code=400, detail=clean_msg)
        if "private" in clean_msg.lower():
            raise HTTPException(status_code=400, detail=clean_msg)
        if "unavailable" in clean_msg.lower():
            raise HTTPException(status_code=404, detail=clean_msg)
        raise HTTPException(status_code=500, detail=clean_msg)


@app.get("/api/download")
async def download_file(
    url: str = Query(...),
    format_id: str = Query(...),
    task_id: str = Query(default=""),
    include_subtitles: bool = Query(default=False),
    request: Request = None,
) -> StreamingResponse:
    # Rate limiting
    client_ip = request.client.host if request.client else "unknown" if request else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please try again in a moment.")

    # Validate task_id (#1)
    if not task_id:
        task_id = str(uuid4())
    if not is_valid_task_id(task_id):
        raise HTTPException(status_code=400, detail="Invalid task_id format")

    # Validate URL server-side (#3)
    from schemas import is_valid_youtube_url
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Only YouTube URLs are allowed")

    # Validate format_id (#4)
    from schemas import is_valid_format_id
    if not is_valid_format_id(format_id):
        raise HTTPException(status_code=400, detail="Invalid format")

    # Cleanup old tasks periodically
    _cleanup_old_tasks()

    try:
        # Inisialisasi progress
        task_progress[task_id] = (
            DownloadStatus(task_id=task_id, status="downloading", progress=0.0),
            time.time(),
        )

        def update_progress(pct: float) -> None:
            task_progress[task_id] = (
                DownloadStatus(task_id=task_id, status="downloading", progress=round(pct, 1)),
                time.time(),
            )

        # Download file
        filepath = await downloader.download(
            url, format_id, task_id, update_progress, include_subtitles
        )

        if not filepath or not os.path.exists(filepath):
            task_progress[task_id] = (
                DownloadStatus(task_id=task_id, status="error", progress=0, error_msg="File not found after download"),
                time.time(),
            )
            raise HTTPException(status_code=500, detail="Download failed: file not found.")

        # Tandai selesai download (yt-dlp), mulai streaming ke client
        task_progress[task_id] = (
            DownloadStatus(task_id=task_id, status="streaming", progress=100.0, filename=os.path.basename(filepath)),
            time.time(),
        )

        # Tentukan content type
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".mp3":
            content_type = "audio/mpeg"
        elif ext in (".opus", ".ogg"):
            content_type = "audio/opus"
        else:
            content_type = "video/mp4"

        # Sanitize filename (#14)
        filename = os.path.basename(filepath)
        clean_name = filename.split("_", 1)[1] if "_" in filename else filename
        clean_name = re.sub(r"[^\w\-. ]", "_", clean_name)[:200]

        # Stream file lalu hapus setelah selesai
        async def file_streamer():
            try:
                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(1024 * 64)
                        if not chunk:
                            break
                        yield chunk
            finally:
                # Tandai benar-benar selesai setelah file di-stream
                task_progress[task_id] = (
                    DownloadStatus(task_id=task_id, status="done", progress=100.0, filename=os.path.basename(filepath)),
                    time.time(),
                )
                try:
                    os.remove(filepath)
                except OSError as e:
                    logger.warning("Failed to remove file %s: %s", filepath, e)

        encoded_name = quote(clean_name)
        file_size = os.path.getsize(filepath)
        return StreamingResponse(
            file_streamer(),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename*=utf-8''{encoded_name}",
                "Content-Length": str(file_size),
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error downloading file")
        clean_msg = sanitize_error_message(str(e))
        task_progress[task_id] = (
            DownloadStatus(task_id=task_id, status="error", progress=0, error_msg=clean_msg),
            time.time(),
        )
        raise HTTPException(status_code=500, detail=clean_msg)


@app.get("/api/progress/{task_id}")
async def progress_stream(task_id: str) -> StreamingResponse:
    # Validate task_id format (#20)
    if not is_valid_task_id(task_id):
        raise HTTPException(status_code=400, detail="Invalid task_id format")

    async def event_generator():
        for _ in range(SSE_MAX_ITERATIONS):  # Timeout after 5 minutes (#11)
            entry = task_progress.get(task_id)
            if entry:
                status, _ = entry
                yield f"data: {status.model_dump_json()}\n\n"
                if status.status in ("done", "error", "streaming"):
                    break
            else:
                payload = json.dumps(
                    {"task_id": task_id, "status": "pending", "progress": 0}
                )
                yield f"data: {payload}\n\n"
            await asyncio.sleep(0.5)
        else:
            # Timeout reached
            yield f"data: {json.dumps({'task_id': task_id, 'status': 'error', 'error_msg': 'Timeout'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# --- Static files serving (Monolith) ---
DIST_DIR = Path(__file__).parent / "dist"

if DIST_DIR.exists():
    if (DIST_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        # Path traversal guard (#2)
        file_path = (DIST_DIR / full_path).resolve()
        if not str(file_path).startswith(str(DIST_DIR.resolve())):
            raise HTTPException(status_code=403, detail="Forbidden")
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(DIST_DIR / "index.html")
