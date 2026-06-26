<template>
  <div class="relative min-h-screen">
    <!-- Background: kawaii dot pattern is on body via CSS -->

    <!-- Header -->
    <header class="sticky top-0 z-20">
      <div class="card-kawaii" style="border-radius: 0; border-left: none; border-right: none; border-top: none;">
        <div class="max-w-[680px] mx-auto px-4 sm:px-6 py-5 flex items-center gap-4">
          <!-- Kawaii play icon -->
          <div
            class="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0"
            style="background: linear-gradient(135deg, #1fb89a, #38a3d6); box-shadow: 0 4px 16px rgba(31, 184, 154, 0.4);"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6 text-white"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M8 5v14l11-7z" />
            </svg>
          </div>
          <!-- Header Text -->
          <div class="flex flex-col flex-1">
            <h1 class="text-2xl sm:text-[1.7rem] font-extrabold tracking-tight leading-tight">
              <span class="text-gradient">KEI</span>
              <span class="jp-display text-gradient"> ダウンローダー</span>
            </h1>
            <p class="text-xs jp-label mt-0.5" style="color: var(--color-muted);">
              動画・音楽ダウンロード · Download Video & Audio
            </p>
          </div>
          <!-- Settings Button -->
          <button
            class="w-10 h-10 flex items-center justify-center rounded-full transition-all cursor-pointer"
            style="color: var(--color-muted);"
            @click="showSettings = true"
            @mouseenter="$event.target.style.color = 'var(--color-accent)'; $event.target.style.background = 'var(--color-bg-surface2)'"
            @mouseleave="$event.target.style.color = 'var(--color-muted)'; $event.target.style.background = 'transparent'"
            title="設定 · Pengaturan"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="relative z-10 max-w-[680px] mx-auto px-4 sm:px-6 py-10 space-y-6">
      <Transition name="slide-fade" mode="out-in">
        <!-- State: idle / error -->
        <UrlInput v-if="status === 'idle' || status === 'error'" />

        <!-- State: loading (kawaii skeleton) -->
        <div
          v-else-if="status === 'loading'"
          class="card-kawaii p-6 space-y-4"
        >
          <div class="animate-shimmer h-[200px] rounded-xl"></div>
          <div class="animate-shimmer h-12 rounded-xl"></div>
          <div class="grid grid-cols-2 gap-3">
            <div class="animate-shimmer h-24 rounded-xl"></div>
            <div class="animate-shimmer h-24 rounded-xl"></div>
          </div>
        </div>

        <!-- State: selecting -->
        <template v-else-if="status === 'selecting'">
          <PlaylistSelector
            v-if="videoInfo?.is_playlist"
            :video-info="videoInfo"
            @start-batch-download="handleStartBatchDownload"
            @reset="handleReset"
          />
          <FormatSelector
            v-else
            :video-info="videoInfo"
            :selected-type="selectedType"
            :selected-format="selectedFormat"
            @select-type="selectType"
            @select-format="selectFormat"
            @start-download="handleStartDownload"
            @reset="handleReset"
          />
        </template>

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
          class="card-kawaii p-8 text-center space-y-6 animate-bounce-in"
        >
          <div
            class="w-20 h-20 mx-auto rounded-full flex items-center justify-center"
            style="background: rgba(134, 239, 172, 0.2);"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-10 w-10"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              style="color: var(--color-success);"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <div class="space-y-2">
            <h2 class="text-2xl font-extrabold text-gradient">完了！ · Selesai!</h2>
            <p class="text-sm jp-display" style="color: var(--color-muted);">
              (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Download berhasil! File tersimpan di folder download browser.
            </p>
          </div>
          <button
            id="btn-download-again"
            class="btn-primary"
            @click="handleReset"
          >
            ✦ <span class="jp-label">もう一度 · Download Lagi</span>
          </button>
        </div>
      </Transition>

      <!-- Download history -->
      <DownloadHistory v-if="history.length > 0" :history="history" />
    </main>

    <!-- Footer -->
    <footer class="relative z-10 pb-6 px-4 sm:px-6">
      <div class="max-w-[680px] mx-auto px-4 py-3" style="border-top: 1px solid var(--color-border);">
        <p class="text-center text-xs" style="color: var(--color-text-muted);">
          <span class="jp-label">作られた</span> Vue 3 + FastAPI + yt-dlp
        </p>
      </div>
    </footer>

    <!-- Modals -->
    <Transition name="modal">
      <SettingsModal v-if="showSettings" @close="showSettings = false" />
    </Transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
import UrlInput from "./components/UrlInput.vue";
import FormatSelector from "./components/FormatSelector.vue";
import PlaylistSelector from "./components/PlaylistSelector.vue";
import ProgressBar from "./components/ProgressBar.vue";
import DownloadHistory from "./components/DownloadHistory.vue";
import SettingsModal from "./components/SettingsModal.vue";
import { useDownloader } from "./composables/useDownloader";

const showSettings = ref(false);

const {
  videoInfo,
  selectedType,
  selectedFormat,
  status,
  progress,
  history,
  handleStartDownload,
  handleStartBatchDownload,
  handleReset,
  selectType,
  selectFormat,
} = useDownloader();
</script>
