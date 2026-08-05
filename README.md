# KEI Downloader

<p align="center">
  <b>🌐 Select Language / Pilih Bahasa</b>
</p>

---

<details open>
  <summary><b>🇮🇩 Bahasa Indonesia</b> (Klik untuk membuka/menutup)</summary>
  <br>

Aplikasi web untuk mengunduh video dan audio dari YouTube. Dibangun dengan arsitektur **Monolith** yang efisien, menggabungkan backend FastAPI dan frontend Vue 3 dengan antarmuka modern bergaya **Glassmorphism**.

**Stack:** Vue 3 + Tailwind CSS v4 (Frontend) · FastAPI + yt-dlp (Backend)

### Fitur

- **Glassmorphism UI** — Antarmuka modern dengan efek transparan, animasi transisi halus, dan desain responsif.
- **Resolusi hingga 4K** — Deteksi otomatis format video terbaik hingga 2160p, termasuk format DASH & Ultrawide.
- **Download Playlist** — Paste URL Playlist, pilih video yang diinginkan, lalu download secara batch berurutan.
- **Embed Subtitle & Metadata** — Otomatis download dan tanamkan subtitle (ID/EN), gambar sampul album (cover art), dan metadata ID3 ke dalam file MP3, OPUS, M4A, dan MP4.
- **Progress Real-time** — Progress bar yang sinkron dengan proses download sebenarnya via Server-Sent Events (SSE).
- **Pengaturan Tersimpan** — Preferensi (Audio/Video default, Subtitle) tersimpan di browser.
- **Riwayat Download** — Menampilkan 3 riwayat download terakhir.

---

### Persyaratan Sistem

- **Python 3.10+**
- **Node.js 18+**
- **ffmpeg** — Wajib terinstall dan tersedia di system PATH.  
  Download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Cek apakah ffmpeg sudah terinstall:
```bash
ffmpeg -version
```
> Aplikasi ini juga otomatis memindai lokasi umum instalasi ffmpeg (WinGet, Scoop, Chocolatey) di Windows.

---

### Struktur Proyek (Monolith)

```text
Kei-Downloader/
├── dist/                  # Output build frontend (disajikan oleh FastAPI)
├── public/                # Asset statis frontend (background, icon)
├── src/                   # Source code Vue 3 (Components, Stores, Composables)
├── downloader.py          # Logika downloader yt-dlp & penanganan ffmpeg
├── main.py                # Server FastAPI & pengelola API & static files
├── schemas.py             # Schema Pydantic
├── index.html             # Entrypoint HTML Vite
├── package.json           # Dependencies Node.js (Vue, Vite, Tailwind CSS v4)
├── requirements.txt       # Dependencies Python (FastAPI, yt-dlp, uvicorn, mutagen)
└── vite.config.js         # Konfigurasi Vite
```

---

### Instalasi & Menjalankan

#### 1. Clone & Setup Dependencies

```bash
git clone https://github.com/RissN/Kei-Downloader.git
cd Kei-Downloader

# Install dependencies Node.js
npm install

# Buat & aktifkan virtual environment Python
python -m venv .venv
.venv\Scripts\activate      # Windows (PowerShell)
# source .venv/bin/activate # macOS/Linux

# Install dependencies Python
pip install -r requirements.txt
```

#### 2. Build Frontend & Menjalankan Server Monolith

```bash
# Build frontend Vue ke folder dist/
npm run build

# Jalankan server FastAPI (Secara otomatis me-serve API dan Frontend)
python -m uvicorn main:app --reload --port 8000
```

Buka browser di: **http://localhost:8000**

---

#### Mode Development (Hot Reload UI)

Jika Anda ingin melakukan pengembangan UI secara langsung (*live editing*):

```bash
# Terminal 1 (Backend API):
python -m uvicorn main:app --reload --port 8000

# Terminal 2 (Vite Dev Server):
npm run dev
```

Akses frontend versi dev di: **http://localhost:5173**

---

### Cara Penggunaan

1. **Pengaturan (opsional):** Klik ikon gear di pojok kanan atas untuk mengatur tipe default (Video/Audio) dan mengaktifkan Embed Subtitle.
2. **Download Video:**
   - Paste URL YouTube ke kolom input.
   - Klik **"Cek Video"** untuk mengambil info video.
   - Pilih format dan resolusi yang diinginkan.
   - Klik **"Unduh Sekarang"** untuk mulai download.
3. **Download Playlist:**
   - Paste URL Playlist YouTube, lalu klik **"Cek Video"**.
   - Centang video yang ingin diunduh dari daftar yang muncul.
   - Pilih format (Video/Audio), lalu klik **"Download (N)"**.
   - Aplikasi akan mengunduh secara berurutan.

---

### Troubleshooting

- **`ffmpeg tidak ditemukan di PATH`**  
  Pastikan ffmpeg sudah terinstall. Di Windows, coba `winget install ffmpeg` lalu restart terminal.

- **`Fatal error in launcher: Unable to create process`**  
  Jalankan server uvicorn menggunakan `python -m uvicorn main:app --reload --port 8000` (bukan memanggil `uvicorn` langsung).

- **Progress bar tidak bergerak?**  
  Pastikan backend FastAPI sedang berjalan di port 8000. Progress tracking menggunakan SSE (Server-Sent Events) untuk memantau proses download secara real-time.

</details>

<br>

<details>
  <summary><b>🇬🇧 English</b> (Click to open/close)</summary>
  <br>

A web application to download video and audio from YouTube. Built with an efficient **Monolith** architecture, pairing a FastAPI backend and a Vue 3 frontend with a sleek **Cyber-Sunset Glassmorphism** design.

**Stack:** Vue 3 + Tailwind CSS v4 (Frontend) · FastAPI + yt-dlp (Backend)

### Features

- **Glassmorphism UI** — Modern interface with transparent glass cards, smooth transition animations, and responsive layout.
- **Up to 4K Resolution** — Auto-detects optimal video resolutions up to 2160p (4K), including DASH & Ultrawide formats.
- **Playlist Download** — Paste a YouTube playlist URL, select desired videos, and batch download sequentially.
- **Embed Subtitles & Metadata** — Automatically downloads & embeds subtitles (ID/EN), album cover art, and ID3 metadata into MP3, OPUS, M4A, and MP4 files.
- **Real-time Progress** — Accurate server-side progress tracking via Server-Sent Events (SSE).
- **Persistent Settings** — Preferences (default media type, subtitle embedding) stored locally in browser.
- **Download History** — Quick view of your 3 most recent downloads.

---

### System Requirements

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

### Project Structure (Monolith)

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

### Installation & Running

#### 1. Clone & Setup Dependencies

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

#### 2. Build Frontend & Run Monolith Server

```bash
# Build Vue frontend into dist/ directory
npm run build

# Run FastAPI server (serves both API and Frontend)
python -m uvicorn main:app --reload --port 8000
```

Open your browser at: **http://localhost:8000**

---

#### Development Mode (Hot Reload UI)

For active UI development and live editing:

```bash
# Terminal 1 (Backend API):
python -m uvicorn main:app --reload --port 8000

# Terminal 2 (Vite Dev Server):
npm run dev
```

Access the dev server at: **http://localhost:5173**

---

### How to Use

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

### Troubleshooting

- **`ffmpeg module or command not found`**  
  Ensure ffmpeg is installed and added to PATH. On Windows, run `winget install ffmpeg` and restart terminal.

- **`Fatal error in launcher: Unable to create process`**  
  Launch uvicorn using `python -m uvicorn main:app --reload --port 8000`.

- **Progress bar stuck?**  
  Ensure the FastAPI server is running on port 8000. Progress tracking relies on SSE (Server-Sent Events) for real-time progress.

</details>

---

*Built with Vue 3 + FastAPI + yt-dlp*
