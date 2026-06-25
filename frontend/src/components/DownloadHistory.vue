<template>
  <div v-if="history.length" class="animate-fade-in space-y-4">
    <!-- Section header -->
    <div class="flex items-center justify-between">
      <h3 class="text-white font-bold text-base">Riwayat Download</h3>
      <button
        id="btn-clear-history"
        class="text-xs text-muted hover:text-danger transition-colors cursor-pointer"
        @click="clearHistory"
      >
        Hapus riwayat
      </button>
    </div>

    <!-- List -->
    <div class="space-y-2">
      <div
        v-for="(item, idx) in history"
        :key="idx"
        class="flex items-center gap-3 p-3 bg-surface border border-edge rounded-xl"
      >
        <!-- Thumbnail -->
        <img
          v-if="item.thumbnail"
          :src="item.thumbnail"
          :alt="item.title"
          class="w-[52px] h-[36px] object-cover rounded-md shrink-0 bg-edge"
        />
        <div
          v-else
          class="w-[52px] h-[36px] bg-edge rounded-md shrink-0 flex items-center justify-center text-muted text-xs"
        >
          ▶
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-white text-sm font-medium truncate">{{ item.title }}</p>
          <div class="flex items-center gap-2 mt-0.5">
            <span
              class="text-[10px] font-bold px-1.5 py-0.5 rounded"
              :class="[
                item.type === 'video'
                  ? 'bg-accent/20 text-accent'
                  : 'bg-blue-500/20 text-blue-400',
              ]"
            >
              {{ item.type === "video" ? "VIDEO" : "AUDIO" }}
            </span>
            <span class="text-muted text-xs">{{ item.quality }}</span>
          </div>
        </div>

        <!-- Relative time -->
        <span class="text-muted text-xs shrink-0">
          {{ relativeTime(item.timestamp) }}
        </span>
      </div>
    </div>
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
