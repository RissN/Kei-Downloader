# KEI Downloader

Aplikasi web untuk mengunduh video dan audio dari YouTube. Dibangun dengan antarmuka modern bergaya **Glassmorphism** yang bersih dan responsif.

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

- **Python 3.11+**
- **Node.js 18+**
- **ffmpeg** — Wajib terinstall dan tersedia di system PATH.
  Download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Cek apakah ffmpeg sudah terinstall:
```bash
ffmpeg -version
```
> Aplikasi ini juga otomatis memindai lokasi umum instalasi ffmpeg (WinGet, Scoop, Chocolatey) di Windows.

---

## Instalasi & Menjalankan

### 1. Clone & Setup Backend

```bash
git clone https://github.com/RissN/Kei-Downloader.git
cd Kei-Downloader/backend

# Buat & aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Jalankan server API
uvicorn main:app --reload --port 8000
```

### 2. Setup Frontend

Buka **terminal baru** (biarkan backend tetap berjalan):

```bash
cd Kei-Downloader/frontend
npm install
npm run dev
```

### 3. Akses Aplikasi

Buka browser: **http://localhost:5173**

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

- **Resolusi 1080p/4K tidak muncul?**
  Sistem sudah mendeteksi otomatis via format_note dan lebar video. Pastikan video tersedia dalam resolusi tersebut di YouTube.

- **Progress bar tidak bergerak?**
  Pastikan backend (`uvicorn`) sedang berjalan di port 8000. Progress tracking menggunakan SSE (Server-Sent Events) untuk memantau proses download secara real-time.

---

*Dibuat dengan Vue 3 + FastAPI + yt-dlp*
