# YT Downloader

Aplikasi web untuk download video dan audio dari YouTube. Pilih kualitas video hingga 1080p atau konversi ke MP3 dengan bitrate pilihan.

**Stack:** Vue 3 + Tailwind CSS v4 (frontend) · FastAPI + yt-dlp (backend)

---

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **ffmpeg** — wajib terinstall dan tersedia di PATH  
  Download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Cek apakah ffmpeg sudah terinstall:

```bash
ffmpeg -version
```

---

## Instalasi

### 1. Clone & masuk ke folder project

```bash
cd yt-downloader
```

### 2. Setup Backend

```bash
cd backend

# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Frontend

```bash
cd frontend
npm install
```

---

## Menjalankan Aplikasi

Buka **2 terminal** terpisah:

### Terminal 1 — Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

### Akses Aplikasi

Buka browser dan pergi ke: **http://localhost:5173**

---

## Cara Penggunaan

1. Paste URL YouTube ke kolom input
2. Klik "Ambil Info" atau tekan Enter (auto-submit saat paste)
3. Pilih tab **Video** atau **Audio**
4. Pilih kualitas yang diinginkan
5. Klik "Mulai Download"
6. Tunggu progress bar selesai — file otomatis tersimpan di folder download browser

---

## Troubleshooting

### ffmpeg tidak ditemukan

```
⚠️ WARNING: ffmpeg tidak ditemukan di PATH
```

Pastikan ffmpeg sudah terinstall dan ditambahkan ke system PATH. Restart terminal setelah mengubah PATH.

### CORS Error

Pastikan backend berjalan di port `8000` dan frontend di port `5173`. Jika menggunakan port berbeda, sesuaikan konfigurasi CORS di `backend/main.py`.

### Video tidak bisa diunduh

- Pastikan URL YouTube valid dan video tidak bersifat privat
- Update yt-dlp ke versi terbaru: `pip install -U yt-dlp`
- Beberapa video mungkin dibatasi berdasarkan region

### Port sudah digunakan

```bash
# Cari proses yang menggunakan port
# Windows:
netstat -ano | findstr :8000
# Linux/macOS:
lsof -i :8000
```

---

## Struktur Project

```
yt-downloader/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── downloader.py         # yt-dlp wrapper
│   ├── schemas.py            # Pydantic models
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── composables/      # Vue composables
│   │   ├── services/         # API helper
│   │   ├── stores/           # Pinia store
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── downloads/                 # Output folder (auto-created)
├── .gitignore
└── README.md
```
