<template>
  <div class="min-h-screen bg-base flex flex-col">
    <!-- Header -->
    <header class="w-full border-b border-edge bg-surface/50 backdrop-blur-sm sticky top-0 z-10">
      <div class="max-w-[760px] mx-auto px-4 py-4 flex items-center gap-3">
        <!-- YouTube-style play icon -->
        <div class="w-9 h-9 bg-accent rounded-lg flex items-center justify-center shrink-0">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5 text-white"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
        <h1 class="text-white font-extrabold text-lg tracking-tight">
          YT Downloader
        </h1>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 w-full max-w-[760px] mx-auto px-4 py-8 space-y-8">
      <!-- State: idle / error -->
      <UrlInput v-if="status === 'idle' || status === 'error'" />

      <!-- State: loading (skeleton) -->
      <div v-else-if="status === 'loading'" class="space-y-4 animate-fade-in">
        <div class="animate-shimmer h-[200px] rounded-2xl"></div>
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
      <div v-else-if="status === 'done'" class="animate-fade-in text-center space-y-6">
        <div class="w-20 h-20 mx-auto bg-success/10 rounded-full flex items-center justify-center">
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
          <h2 class="text-white text-2xl font-bold">Download Berhasil!</h2>
          <p class="text-muted text-sm">
            File sedang disimpan ke folder download browser kamu.
          </p>
        </div>
        <button
          id="btn-download-again"
          class="px-8 py-3 bg-accent hover:bg-accent-hover text-white font-semibold text-sm rounded-xl transition-all duration-200 active:scale-[0.98] cursor-pointer"
          @click="handleReset"
        >
          Download lagi
        </button>
      </div>

      <!-- Download history -->
      <div v-if="history.length > 0" class="border-t border-edge pt-8">
        <DownloadHistory />
      </div>
    </main>

    <!-- Footer -->
    <footer class="w-full border-t border-edge py-4">
      <p class="text-center text-muted text-xs">
        Dibuat dengan ❤️ menggunakan Vue 3 + FastAPI + yt-dlp
      </p>
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
