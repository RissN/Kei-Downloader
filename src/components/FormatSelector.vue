<template>
  <div class="space-y-4 animate-fade-in">
    <!-- Card 1: Video Info Preview -->
    <div class="card p-4 sm:p-5">
      <div class="flex flex-col sm:flex-row items-center gap-4">
        <!-- Thumbnail -->
        <div class="relative w-full sm:w-52 aspect-video rounded-xl overflow-hidden shrink-0 shadow-md" style="border: 1px solid var(--color-border);">
          <img
            v-if="videoInfo?.thumbnail"
            :src="videoInfo.thumbnail"
            :alt="videoInfo?.title"
            class="w-full h-full object-cover"
          />
          <!-- Duration badge -->
          <span
            v-if="videoInfo?.duration"
            class="absolute bottom-2 right-2 text-white text-[11px] font-bold px-2 py-0.5 rounded-md"
            style="background: rgba(14, 14, 28, 0.85); backdrop-filter: blur(4px);"
          >
            {{ formatDuration(videoInfo.duration) }}
          </span>
        </div>

        <!-- Info & Title -->
        <div class="flex-1 min-w-0 space-y-1.5 text-center sm:text-left">
          <span
            class="inline-block px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider"
            style="background: var(--color-accent-soft); color: var(--color-accent);"
          >
            YouTube Video
          </span>
          <h2 class="font-extrabold text-base sm:text-lg leading-snug line-clamp-2" style="color: var(--color-text);">
            {{ videoInfo?.title }}
          </h2>
        </div>
      </div>
    </div>

    <!-- Card 2: Format Options & Actions -->
    <div class="card p-5 sm:p-6 space-y-5">
      <!-- Section Title & Tabs Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-1">
        <div class="space-y-0.5">
          <h3 class="text-lg font-extrabold text-gradient text-display">Pilih Format & Kualitas</h3>
          <p class="text-xs" style="color: var(--color-muted);">Pilih format media yang sesuai untuk diunduh</p>
        </div>

        <!-- Tab switcher -->
        <div class="tab-group shrink-0 sm:w-auto w-full">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            :id="`tab-${tab.value}`"
            :class="[
              selectedType === tab.value ? 'tab-active' : '',
            ]"
            @click="$emit('selectType', tab.value)"
          >
            {{ tab.icon }}
            <span class="text-label">{{ tab.label }}</span>
          </button>
        </div>
      </div>

      <!-- Audio Codec Selector -->
      <div v-if="selectedType === 'audio'" class="flex items-center justify-between bg-black/25 px-3 py-2 rounded-xl border border-[var(--color-border)] animate-fade-in">
        <span class="text-xs font-bold text-[var(--color-muted)]">Format Audio:</span>
        <select
          v-model="selectedAudioCodec"
          class="appearance-none bg-[var(--color-bg-surface)] border border-[var(--color-border)] rounded-lg px-3 py-1 pr-7 text-xs font-bold text-[var(--color-text)] outline-none focus:border-[var(--color-accent)] cursor-pointer"
        >
          <option value="mp3">MP3 (.mp3)</option>
          <option value="opus">OPUS (.opus)</option>
        </select>
      </div>

      <!-- Format Grid (Spreads horizontally into 2-4 columns) -->
      <TransitionGroup
        name="format-list"
        tag="div"
        class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 max-h-[300px] overflow-y-auto pr-1"
      >
        <button
          v-for="(fmt, idx) in filteredFormats"
          :key="fmt.format_id"
          :id="`format-${fmt.format_id}`"
          class="text-left transition-all duration-200 cursor-pointer"
          :class="[
            selectedFormat?.format_id === fmt.format_id
              ? 'format-card format-card-selected'
              : 'format-card',
          ]"
          :style="{ animationDelay: `${idx * 40}ms` }"
          @click="$emit('selectFormat', fmt)"
        >
          <!-- Best badge -->
          <span
            v-if="idx === 0"
            class="badge-best absolute -top-2 right-2 text-[9px] px-2 py-0.5"
          >
            Terbaik
          </span>

          <div class="space-y-1">
            <span class="font-bold text-sm sm:text-base block truncate" style="color: var(--color-text);">
              {{ fmt.quality_label }}
            </span>
            <div class="flex items-center gap-1.5 text-[11px]" style="color: var(--color-muted);">
              <span
                class="px-1.5 py-0.5 rounded-full text-[9px] font-bold uppercase shrink-0"
                style="background: rgba(255, 255, 255, 0.1); color: var(--color-muted);"
              >
                .{{ fmt.ext }}
              </span>
              <span v-if="fmt.filesize_approx" class="truncate">
                ~{{ formatSize(fmt.filesize_approx) }}
              </span>
            </div>
          </div>
        </button>
      </TransitionGroup>

      <!-- Action Buttons -->
      <div class="flex gap-3 pt-2">
        <button
          id="btn-change-url"
          type="button"
          class="flex-1 btn-ghost"
          @click="$emit('reset')"
        >
          <span class="text-label">Kembali</span>
        </button>
        <button
          id="btn-start-download"
          type="button"
          :disabled="!selectedFormat"
          class="flex-[2] btn-primary"
          :style="!selectedFormat ? 'background: var(--color-text-muted); box-shadow: none;' : ''"
          @click="$emit('startDownload')"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
          <span class="text-label">Unduh</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  videoInfo: { type: Object, default: null },
  selectedType: { type: String, default: "video" },
  selectedFormat: { type: Object, default: null },
});

const emit = defineEmits(["selectType", "selectFormat", "startDownload", "reset"]);

const tabs = [
  { value: "video", label: "Video", icon: "🎬 " },
  { value: "audio", label: "Audio", icon: "🎵 " },
];

const selectedAudioCodec = ref("mp3");

// Reset codec to mp3 when switching back to audio tab (optional, but good for UX)
watch(() => props.selectedType, (newVal) => {
  if (newVal === 'audio') {
    selectedAudioCodec.value = "mp3";
  }
});

const filteredFormats = computed(() => {
  if (!props.videoInfo?.formats) return [];
  return props.videoInfo.formats.filter((f) => {
    if (f.type !== props.selectedType) return false;
    if (props.selectedType === 'audio' && f.ext) {
      return f.ext === selectedAudioCodec.value;
    }
    return true;
  });
});

/**
 * Format detik ke mm:ss atau hh:mm:ss.
 * @param {number} seconds
 * @returns {string}
 */
function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const mm = String(m).padStart(2, "0");
  const ss = String(s).padStart(2, "0");
  return h > 0 ? `${h}:${mm}:${ss}` : `${m}:${ss}`;
}

/**
 * Format bytes ke label human-readable.
 * @param {number} bytes
 * @returns {string}
 */
function formatSize(bytes) {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  if (bytes < 1024 * 1024 * 1024)
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}
</script>
