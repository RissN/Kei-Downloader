# KEI Downloader

Aplikasi web untuk mengunduh video dan audio dari YouTube. Dibangun dengan arsitektur **Monolith** yang efisien, menggabungkan backend FastAPI dan frontend Vue 3 dengan antarmuka modern bergaya **Glassmorphism**.

**Stack:** Vue 3 + Tailwind CSS v4 (Frontend) · FastAPI + yt-dlp (Backend)

---

## Fitur

- **Glassmorphism UI** — Antarmuka modern dengan efek transparan, animasi transisi halus, dan desain responsif.
- **Resolusi hingga 4K** — Deteksi otomatis format video terbaik hingga 2160p, termasuk format DASH & Ultrawide.
- **Download Playlist** — Paste URL Playlist, pilih video yang diinginkan, lalu download secara batch berurutan.
- **Embed Subtitle** — Otomatis download dan tanamkan subtitle (ID/EN) ke dalam file MP4 menggunakan ffmpeg.
- **Progress Real-time** — Progress bar yang sinkron dengan proses download sebenarnya (server-side download + transfer file ke browser).
- **Pengaturan Tersimpan** — Preferensi (Audio/Video default, Subtitle) tersimpan di browser.
- **Riwayat Download** — Catatan download terakhir tersimpan secara lokal.

---

## Persyaratan Sistem

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

## Struktur Proyek (Monolith)

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
├── requirements.txt       # Dependencies Python (FastAPI, yt-dlp, uvicorn)
└── vite.config.js         # Konfigurasi Vite
```

---

## Instalasi & Menjalankan

### 1. Clone & Setup Dependencies

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

### 2. Build Frontend & Menjalankan Server Monolith

```bash
# Build frontend Vue ke folder dist/
npm run build

# Jalankan server FastAPI (Secara otomatis me-serve API dan Frontend)
python -m uvicorn main:app --reload --port 8000
```

Buka browser di: **http://localhost:8000**

---

### Mode Development (Hot Reload UI)

Jika Anda ingin melakukan pengembangan UI secara langsung (*live editing*):

```bash
# Terminal 1 (Backend API):
python -m uvicorn main:app --reload --port 8000

# Terminal 2 (Vite Dev Server):
npm run dev
```

Akses frontend versi dev di: **http://localhost:5173**

---

## Cara Penggunaan

1. **Pengaturan (opsional):** Klik ikon gear di pojok kanan atas untuk mengatur tipe default (Video/Audio) dan mengaktifkan Embed Subtitle.
2. **Download Video:**
   - Paste URL YouTube ke kolom input.
   - Klik **"Cek Video"** untuk mengambil info video.
   - Pilih format dan resolusi yang diinginkan.
   - Klik **"Unduh"** untuk mulai download.
3. **Download Playlist:**
   - Paste URL Playlist YouTube, lalu klik **"Cek Video"**.
   - Centang video yang ingin diunduh dari daftar yang muncul.
   - Pilih format (Video/Audio), lalu klik **"Download (N)"**.
   - Aplikasi akan mengunduh secara berurutan.

---

## Troubleshooting

- **`ffmpeg tidak ditemukan di PATH`**
  Pastikan ffmpeg sudah terinstall. Di Windows, coba `winget install ffmpeg` lalu restart terminal.

- **`Fatal error in launcher: Unable to create process`**
  Jalankan server uvicorn menggunakan `python -m uvicorn main:app --reload --port 8000` (bukan memanggil `uvicorn` langsung).

- **Progress bar tidak bergerak?**
  Pastikan backend FastAPI sedang berjalan di port 8000. Progress tracking menggunakan SSE (Server-Sent Events) untuk memantau proses download secara real-time.

---

*Dibuat dengan Vue 3 + FastAPI + yt-dlp*
