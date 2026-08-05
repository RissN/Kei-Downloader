"""FastAPI application — YouTube Downloader backend."""

import asyncio
import json
import os
import traceback
from pathlib import Path
from typing import Dict
from urllib.parse import quote
from uuid import uuid4

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException, Query
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from downloader import YTDownloader
from schemas import DownloadStatus, InfoRequest

app = FastAPI(title="YT Downloader API")

# --- CORS ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length"],
)

# --- Global state ---
task_progress: Dict[str, DownloadStatus] = {}
downloader = YTDownloader()

DOWNLOAD_DIR = Path(__file__).parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)


# --- Startup check ---
@app.on_event("startup")
async def startup_check() -> None:
    from downloader import FFMPEG_LOCATION

    if FFMPEG_LOCATION:
        print(f"[OK] ffmpeg ditemukan: {FFMPEG_LOCATION}")
    else:
        print(
            "[WARNING] ffmpeg tidak ditemukan di PATH maupun lokasi umum. "
            "Konversi audio dan merge video akan gagal."
        )


# --- Endpoints ---
@app.get("/api/health")
async def health() -> dict:
    import yt_dlp

    return {"status": "ok", "yt_dlp_version": yt_dlp.version.__version__}


def sanitize_error_message(msg: str) -> str:
    msg_lower = msg.lower()
    if "is not a valid url" in msg_lower or "unsupported url" in msg_lower:
        return "URL YouTube tidak valid atau tidak didukung. Mohon periksa kembali link Anda."
    if "private video" in msg_lower:
        return "Video ini bersifat privat dan tidak dapat diakses."
    if "not available" in msg_lower or "unavailable" in msg_lower:
        return "Video tidak tersedia atau dibatasi di region Anda."
    if "copyright" in msg_lower:
        return "Video ini tidak dapat diunduh karena klaim hak cipta."
    if "sign in to confirm your age" in msg_lower or "age-gated" in msg_lower:
        return "Video ini dibatasi usia oleh YouTube."
    if "file tidak ditemukan" in msg_lower:
        return "Gagal memproses file hasil unduhan. Silakan coba lagi."
    return "Terjadi kesalahan saat memproses video. Silakan coba lagi atau pilih format lain."


@app.post("/api/info")
async def get_info(req: InfoRequest) -> dict:
    try:
        info = await downloader.get_info(req.url)
        return info.model_dump()
    except Exception as e:
        traceback.print_exc()
        clean_msg = sanitize_error_message(str(e))
        if "tidak valid" in clean_msg:
            raise HTTPException(status_code=400, detail=clean_msg)
        if "privat" in clean_msg:
            raise HTTPException(status_code=400, detail=clean_msg)
        if "tidak tersedia" in clean_msg:
            raise HTTPException(status_code=404, detail=clean_msg)
        raise HTTPException(status_code=500, detail=clean_msg)


@app.get("/api/download")
async def download_file(
    url: str = Query(...),
    format_id: str = Query(...),
    task_id: str = Query(default=""),
    include_subtitles: bool = Query(default=False),
) -> StreamingResponse:
    if not task_id:
        task_id = str(uuid4())

    try:
        # Inisialisasi progress
        task_progress[task_id] = DownloadStatus(
            task_id=task_id, status="downloading", progress=0.0
        )

        def update_progress(pct: float) -> None:
            task_progress[task_id] = DownloadStatus(
                task_id=task_id,
                status="downloading",
                progress=round(pct, 1),
            )

        # Download file
        filepath = await downloader.download(
            url, format_id, task_id, update_progress, include_subtitles
        )

        if not filepath or not os.path.exists(filepath):
            task_progress[task_id] = DownloadStatus(
                task_id=task_id,
                status="error",
                progress=0,
                error_msg="File tidak ditemukan setelah download",
            )
            raise HTTPException(status_code=500, detail="Download gagal: file tidak ditemukan.")

        # Tandai selesai download (yt-dlp), mulai streaming ke client
        task_progress[task_id] = DownloadStatus(
            task_id=task_id,
            status="streaming",
            progress=100.0,
            filename=os.path.basename(filepath),
        )

        # Tentukan content type
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".mp3":
            content_type = "audio/mpeg"
        elif ext in (".opus", ".ogg"):
            content_type = "audio/opus"
        else:
            content_type = "video/mp4"
        filename = os.path.basename(filepath)
        # Hapus prefix task_id dari nama file
        clean_name = filename.split("_", 1)[1] if "_" in filename else filename

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
                task_progress[task_id] = DownloadStatus(
                    task_id=task_id,
                    status="done",
                    progress=100.0,
                    filename=os.path.basename(filepath),
                )
                try:
                    os.remove(filepath)
                except OSError:
                    pass

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
        traceback.print_exc()
        clean_msg = sanitize_error_message(str(e))
        task_progress[task_id] = DownloadStatus(
            task_id=task_id, status="error", progress=0, error_msg=clean_msg
        )
        raise HTTPException(status_code=500, detail=clean_msg)


@app.get("/api/progress/{task_id}")
async def progress_stream(task_id: str) -> StreamingResponse:
    async def event_generator():
        while True:
            status = task_progress.get(task_id)
            if status:
                yield f"data: {status.model_dump_json()}\n\n"
                if status.status in ("done", "error", "streaming"):
                    break
            else:
                payload = json.dumps(
                    {"task_id": task_id, "status": "pending", "progress": 0}
                )
                yield f"data: {payload}\n\n"
            await asyncio.sleep(0.5)

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
        file_path = DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(DIST_DIR / "index.html")

