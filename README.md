# ⛩️ KEI Downloader

Aplikasi web modern untuk mengunduh video dan audio dari YouTube. Dirancang dengan **Tema Japanese Glassmorphism (Sky Blue Edition)** yang cerah dan estetis, memberikan pengalaman mengunduh yang cepat, mulus, dan indah dipandang.

**Stack Utama:** Vue 3 + Tailwind CSS v4 (Frontend) · FastAPI + yt-dlp (Backend)

---

## ✨ Fitur Unggulan

- 🎨 **Sky Blue Glassmorphism UI:** Antarmuka tembus pandang yang menyesuaikan dengan latar belakang Anda, dilengkapi dengan animasi transisi yang halus.
- 🎬 **Resolusi hingga 4K Ultrawide:** Sistem deteksi otomatis yang cerdas untuk mengunduh format video terbaik hingga *2160p*, termasuk format *DASH* & *Ultrawide*.
- 🗂️ **Dukungan Playlist Batch:** Paste URL Playlist dan pilih video mana saja yang ingin diunduh. Sistem akan mengantre dan mengunduhnya satu per satu secara berurutan.
- 📝 **Embed Subtitle Otomatis:** Fitur pengaturan untuk secara otomatis mengunduh dan menanamkan (embed) subtitle (ID/EN) ke dalam format mp4 menggunakan `ffmpeg`.
- ⚙️ **Pengaturan Tersimpan:** Atur preferensi Anda (Audio/Video default, Subtitle) dan sistem akan mengingatnya di browser Anda.

---

## ⚙️ Persyaratan Sistem (Prerequisites)

- **Python 3.11+**
- **Node.js 18+**
- **ffmpeg** — **wajib** terinstall dan tersedia di system PATH.  
  Download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Cek apakah ffmpeg sudah terinstall melalui terminal:
```bash
ffmpeg -version
```
*(Catatan: Aplikasi ini juga otomatis memindai lokasi umum instalasi ffmpeg via WinGet/Scoop di Windows).*

---

## 🚀 Instalasi & Menjalankan Aplikasi

### 1. Clone & Setup Backend

```bash
git clone https://github.com/RissN/Kei-Downloader.git
cd Kei-Downloader/backend

# Buat & aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate      # Untuk Windows
# source .venv/bin/activate # Untuk macOS/Linux

# Install dependencies backend
pip install -r requirements.txt

# Jalankan server API (Port 8000)
uvicorn main:app --reload --port 8000
```

### 2. Setup Frontend

Buka **terminal baru** (biarkan backend tetap berjalan):

```bash
cd Kei-Downloader/frontend
npm install

# Jalankan development server
npm run dev
```

### 3. Akses Aplikasi
Buka browser dan kunjungi: **http://localhost:5173**

---

## 📝 Cara Penggunaan

1. **Pengaturan Awal:** Klik ikon ⚙️ (Gear) di pojok kanan atas untuk mengatur tipe *default* (Video/Audio) dan menyalakan fitur *Embed Subtitle*.
2. **Download Single Video:** 
   - Paste URL YouTube (termasuk resolusi tinggi 4K).
   - Klik "Ambil Info" dan pilih resolusi yang muncul.
   - Klik "Mulai Download".
3. **Download Playlist:**
   - Paste URL Playlist YouTube.
   - Layar akan menampilkan daftar video dalam mode *batch selection*.
   - Centang video yang ingin diunduh, lalu tekan "Mulai Download (N)". Aplikasi akan mengunduh secara berurutan.

---

## 🛠️ Troubleshooting

- **`⚠️ WARNING: ffmpeg tidak ditemukan di PATH`**  
  Pastikan ffmpeg sudah terinstall. Jika menggunakan Windows, coba install via `winget install ffmpeg` dan *restart terminal*.
- **Pilihan Resolusi 1080p/4K Tidak Muncul?**  
  Terkadang video dari YouTube diproses perlahan. Namun, sistem kita sudah mendeteksi otomatis *format_note* dan *lebar video* untuk memastikan 4K selalu muncul jika tersedia dari YouTube. Pastikan Anda me-*refresh* URL jika habis menekan batal.

---

*Made with ❤️ using FastAPI & Vue 3*
