# KEI Downloader

<p align="center">
  <a href="README.md">Bahasa Indonesia</a> | <b>English</b>
</p>

A web application to download video and audio from YouTube. Built with an efficient **Monolith** architecture, pairing a FastAPI backend and a Vue 3 frontend with a sleek **Cyber-Sunset Glassmorphism** design.

**Stack:** Vue 3 + Tailwind CSS v4 (Frontend) · FastAPI + yt-dlp (Backend)

---

## Features

- **Glassmorphism UI** — Modern interface with transparent glass cards, smooth transition animations, and responsive layout.
- **Up to 4K Resolution** — Auto-detects optimal video resolutions up to 2160p (4K), including DASH & Ultrawide formats.
- **Playlist Download** — Paste a YouTube playlist URL, select desired videos, and batch download sequentially.
- **Embed Subtitles & Metadata** — Automatically downloads & embeds subtitles (ID/EN) and audio cover art / ID3 metadata into MP3, OPUS, M4A, and MP4 files.
- **Real-time Progress** — Accurate server-side progress bar tracked via Server-Sent Events (SSE).
- **Persistent Settings** — Preferences (default media type, subtitle embedding) stored locally in browser.
- **Download History** — Quick view of your recent downloads (top 3 items displayed).

---

## System Requirements

- **Python 3.10+**
- **Node.js 18+**
- **ffmpeg** — Must be installed and available in system PATH.  
  Download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Check if ffmpeg is installed:
```bash
ffmpeg -version
```
> The application also automatically scans common installation paths on Windows (WinGet, Scoop, Chocolatey).

---

## Project Structure (Monolith)

```text
Kei-Downloader/
├── dist/                  # Built frontend assets (served by FastAPI)
├── public/                # Static assets (background image, icons)
├── src/                   # Vue 3 source code (Components, Stores, Composables)
├── downloader.py          # yt-dlp downloader engine & ffmpeg postprocessing
├── main.py                # FastAPI server, REST API & static file routes
├── schemas.py             # Pydantic schemas
├── index.html             # Vite HTML entrypoint
├── package.json           # Node.js dependencies (Vue 3, Vite, Tailwind CSS v4)
├── requirements.txt       # Python dependencies (FastAPI, yt-dlp, uvicorn, mutagen)
└── vite.config.js         # Vite configuration
```

---

## Installation & Running

### 1. Clone & Setup Dependencies

```bash
git clone https://github.com/RissN/Kei-Downloader.git
cd Kei-Downloader

# Install Node.js dependencies
npm install

# Create & activate Python virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows (PowerShell)
# source .venv/bin/activate # macOS/Linux

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Build Frontend & Run Monolith Server

```bash
# Build Vue frontend into dist/ directory
npm run build

# Run FastAPI server (serves both API and Frontend)
python -m uvicorn main:app --reload --port 8000
```

Open your browser at: **http://localhost:8000**

---

### Development Mode (Hot Reload UI)

For active UI development and live editing:

```bash
# Terminal 1 (Backend API):
python -m uvicorn main:app --reload --port 8000

# Terminal 2 (Vite Dev Server):
npm run dev
```

Access the dev server at: **http://localhost:5173**

---

## How to Use

1. **Settings (Optional):** Click the gear icon in the top right header to set default media type (Video/Audio) or toggle subtitle embedding.
2. **Single Video Download:**
   - Paste YouTube URL into the input field.
   - Click **"Cek Video"** to fetch video details.
   - Choose desired format (Video resolution or Audio codec/bitrate).
   - Click **"Unduh Sekarang"** to start download.
3. **Playlist Download:**
   - Paste YouTube Playlist URL, then click **"Cek Video"**.
   - Check/select videos to download from the list.
   - Choose format (Video/Audio), then click **"Download (N)"**.
   - Downloads proceed sequentially.

---

## Troubleshooting

- **`ffmpeg module or command not found`**  
  Ensure ffmpeg is installed and added to PATH. On Windows, run `winget install ffmpeg` and restart terminal.

- **`Fatal error in launcher: Unable to create process`**  
  Launch uvicorn using `python -m uvicorn main:app --reload --port 8000` (or `.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000`).

- **Progress bar stuck?**  
  Ensure the FastAPI server is running on port 8000. Progress tracking relies on SSE (Server-Sent Events) for real-time progress.

---

*Built with Vue 3 + FastAPI + yt-dlp*
