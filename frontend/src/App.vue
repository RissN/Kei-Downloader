<template>
  <div class="relative min-h-screen">
    <!-- Background: user image + gradient fallback -->
    <div
      class="fixed inset-0 -z-20 bg-cover bg-center bg-no-repeat"
      :style="{
        backgroundImage: `url('/bg/bg.webp'), url('/bg/bg.jpg'), url('/bg/bg.png'), linear-gradient(160deg, #7EC8E3 0%, #A8D8EA 25%, #D4E7F1 50%, #F2E6E9 75%, #FFF5F5 100%)`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }"
    ></div>

    <!-- Soft overlay for text readability -->
    <div class="fixed inset-0 -z-10 bg-gradient-to-b from-white/5 via-transparent to-white/20"></div>

    <!-- Floating decorations (kanji removed as requested) -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
    </div>

    <!-- Header -->
    <header class="sticky top-0 z-20">
      <div class="glass-strong">
        <div class="max-w-[720px] mx-auto px-4 sm:px-6 py-4 flex items-center gap-3">
          <!-- Torii-red play icon -->
          <div
            class="w-10 h-10 bg-accent rounded-xl flex items-center justify-center shrink-0 shadow-lg shadow-accent/25"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5 text-white"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M8 5v14l11-7z" />
            </svg>
          </div>
          <div>
            <h1 class="text-text font-extrabold text-lg tracking-tight">
              KEI
              <span class="text-accent jp-label">DOWNLOADER</span>
            </h1>
            <p class="text-muted text-[10px] tracking-wider jp-label">
              Download Video dan Audio
            </p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="relative z-10 max-w-[720px] mx-auto px-4 sm:px-6 py-8 space-y-6">
      <!-- State: idle / error -->
      <UrlInput v-if="status === 'idle' || status === 'error'" />

      <!-- State: loading (glass skeleton) -->
      <div
        v-else-if="status === 'loading'"
        class="glass rounded-2xl p-6 space-y-4 animate-fade-in"
      >
        <div class="animate-shimmer h-[200px] rounded-xl"></div>
        <div class="animate-shimmer h-12 rounded-xl"></div>
        <div class="grid grid-cols-2 gap-3">
          <div class="animate-shimmer h-24 rounded-xl"></div>
          <div class="animate-shimmer h-24 rounded-xl"></div>
        </div>
      </div>

      <!-- State: selecting -->
      <FormatSelector
        v-else-if="status === 'selecting'"
        :video-info="videoInfo"
        :selected-type="selectedType"
        :selected-format="selectedFormat"
        @select-type="selectType"
        @select-format="selectFormat"
        @start-download="handleStartDownload"
        @reset="handleReset"
      />

      <!-- State: downloading -->
      <ProgressBar
        v-else-if="status === 'downloading'"
        :progress="progress"
        :video-info="videoInfo"
        :selected-format="selectedFormat"
      />

      <!-- State: done -->
      <div
        v-else-if="status === 'done'"
        class="glass rounded-2xl p-8 animate-fade-in text-center space-y-6"
      >
        <div
          class="w-20 h-20 mx-auto bg-success/15 rounded-full flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-10 h-10 text-success"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
        <div class="space-y-2">
          <h2 class="text-text text-2xl font-bold jp-label">Selesai!</h2>
          <p class="text-muted text-sm">
            Download berhasil! File tersimpan di folder download browser.
          </p>
        </div>
        <button
          id="btn-download-again"
          class="px-8 py-3 bg-accent hover:bg-accent-hover text-white font-semibold text-sm rounded-xl transition-all duration-200 active:scale-[0.98] cursor-pointer shadow-lg shadow-accent/20 jp-label"
          @click="handleReset"
        >
          Download Ulang
        </button>
      </div>

      <!-- Download history -->
      <DownloadHistory v-if="history.length > 0" />
    </main>

    <!-- Footer -->
    <footer class="relative z-10 pb-6 px-4 sm:px-6">
      <div class="glass-subtle rounded-xl max-w-[720px] mx-auto px-4 py-3">
        <p class="text-center text-muted/80 text-xs">
          <span class="text-sakura">❤</span>
          <span class="jp-label">Dibuat dengan</span> Vue 3 + FastAPI + yt-dlp
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import UrlInput from "./components/UrlInput.vue";
import FormatSelector from "./components/FormatSelector.vue";
import ProgressBar from "./components/ProgressBar.vue";
import DownloadHistory from "./components/DownloadHistory.vue";
import { useDownloader } from "./composables/useDownloader";

const {
  videoInfo,
  selectedType,
  selectedFormat,
  status,
  progress,
  history,
  handleStartDownload,
  handleReset,
  selectType,
  selectFormat,
} = useDownloader();
</script>
