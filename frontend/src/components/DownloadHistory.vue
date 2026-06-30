<template>
  <div
    v-if="history.length"
    class="card-kawaii p-6 sm:p-8 animate-fade-in space-y-4"
  >
    <!-- Section header -->
    <div class="flex items-center justify-between">
      <div class="space-y-0.5">
        <h3 class="text-base font-extrabold text-gradient jp-display">
          Riwayat Download
        </h3>
        <p class="text-xs" style="color: var(--color-muted);">Riwayat Download</p>
      </div>
      <button
        id="btn-clear-history"
        class="btn-ghost text-xs !py-2 !px-3"
        @click="clearHistory"
      >
        <span class="jp-label">Hapus</span>
      </button>
    </div>

    <!-- List -->
    <div class="space-y-2">
      <div
        v-for="(item, idx) in history"
        :key="idx"
        class="flex items-center gap-3 p-3 rounded-2xl transition-all"
        style="background: var(--color-bg-surface); border: 1px solid var(--color-border);"
        @mouseenter="$event.currentTarget.style.background = 'var(--color-bg-surface2)'"
        @mouseleave="$event.currentTarget.style.background = 'var(--color-bg-surface)'"
      >
        <!-- Thumbnail -->
        <img
          v-if="item.thumbnail"
          :src="item.thumbnail"
          :alt="item.title"
          class="w-[52px] h-[36px] object-cover rounded-lg shrink-0"
        />
        <div
          v-else
          class="w-[52px] h-[36px] rounded-lg shrink-0 flex items-center justify-center text-xs"
          style="background: var(--color-bg-surface2); color: var(--color-muted);"
        >
          ▶
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold truncate" style="color: var(--color-text);">{{ item.title }}</p>
          <div class="flex items-center gap-2 mt-0.5">
            <span
              :class="[
                item.type === 'video'
                  ? 'badge-video'
                  : 'badge-audio',
              ]"
            >
              {{ item.type === "video" ? "Video" : "Audio" }}
            </span>
            <span class="text-xs" style="color: var(--color-text-muted);">{{ item.quality }}</span>
          </div>
        </div>

        <!-- Relative time -->
        <span class="text-xs shrink-0" style="color: var(--color-text-muted);">
          {{ relativeTime(item.timestamp) }}
        </span>
      </div>
    </div>

    <!-- Empty state (for future use if needed) -->
  </div>

  <!-- Empty state when no history -->
  <div
    v-else
    class="card-kawaii p-6 text-center animate-fade-in"
  >
    <p class="jp-display text-sm" style="color: var(--color-text-muted);">
      Belum ada riwayat
    </p>
  </div>
</template>

<script setup>
import { useDownloader } from "../composables/useDownloader";
import { useDownloadStore } from "../stores/downloadStore";

const { history } = useDownloader();
const store = useDownloadStore();

function clearHistory() {
  store.clearHistory();
}

/**
 * Hitung waktu relatif dari timestamp.
 * @param {number} timestamp - Unix ms
 * @returns {string}
 */
function relativeTime(timestamp) {
  const diff = Date.now() - timestamp;
  const seconds = Math.floor(diff / 1000);

  if (seconds < 60) return "Baru saja";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} menit lalu`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} jam lalu`;
  const days = Math.floor(hours / 24);
  return `${days} hari lalu`;
}
</script>
