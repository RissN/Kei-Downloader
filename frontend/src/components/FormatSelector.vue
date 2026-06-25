<template>
  <div class="glass rounded-2xl p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Video preview -->
    <div class="rounded-xl overflow-hidden glass-card">
      <div class="relative">
        <img
          v-if="videoInfo?.thumbnail"
          :src="videoInfo.thumbnail"
          :alt="videoInfo?.title"
          class="w-full aspect-video object-cover"
        />
        <!-- Duration badge -->
        <span
          v-if="videoInfo?.duration"
          class="absolute bottom-2 right-2 bg-black/70 text-white text-xs font-medium px-2 py-0.5 rounded backdrop-blur-sm"
        >
          {{ formatDuration(videoInfo.duration) }}
        </span>
      </div>
      <div class="p-4">
        <h3 class="text-text font-bold text-base leading-snug line-clamp-2">
          {{ videoInfo?.title }}
        </h3>
      </div>
    </div>

    <!-- Tab switcher -->
    <div class="flex glass-subtle rounded-xl p-1 gap-1">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :id="`tab-${tab.value}`"
        class="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 cursor-pointer"
        :class="[
          selectedType === tab.value
            ? 'bg-accent text-white shadow-lg shadow-accent/20'
            : 'text-muted hover:text-text hover:bg-white/30',
        ]"
        @click="$emit('selectType', tab.value)"
      >
        {{ tab.icon }}
        <span class="jp-label">{{ tab.label }}</span>
      </button>
    </div>

    <!-- Format grid -->
    <div
      :class="[
        selectedType === 'video'
          ? 'grid grid-cols-2 gap-3'
          : 'flex flex-col gap-3',
      ]"
    >
      <button
        v-for="(fmt, idx) in filteredFormats"
        :key="fmt.format_id"
        :id="`format-${fmt.format_id}`"
        class="relative p-4 rounded-xl text-left transition-all duration-200 cursor-pointer"
        :class="[
          selectedFormat?.format_id === fmt.format_id
            ? 'bg-accent/10 border-2 border-accent/50 shadow-md shadow-accent/10'
            : 'glass-card',
        ]"
        @click="$emit('selectFormat', fmt)"
      >
        <!-- Best badge -->
        <span
          v-if="idx === 0"
          class="absolute -top-2 right-3 bg-accent text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm jp-label uppercase"
        >
          Terbaik
        </span>

        <div class="space-y-1.5">
          <span class="text-text font-bold text-base">
            {{ fmt.quality_label }}
          </span>
          <div class="flex items-center gap-2 text-xs text-muted">
            <span
              class="px-1.5 py-0.5 bg-black/5 rounded text-[10px] font-semibold uppercase"
            >
              .{{ fmt.ext }}
            </span>
            <span v-if="fmt.filesize_approx">
              ~{{ formatSize(fmt.filesize_approx) }}
            </span>
          </div>
        </div>
      </button>
    </div>

    <!-- Actions -->
    <div class="flex gap-3">
      <button
        id="btn-change-url"
        type="button"
        class="flex-1 py-3 rounded-xl glass-subtle text-muted hover:text-text font-medium text-sm transition-all duration-200 cursor-pointer"
        @click="$emit('reset')"
      >
        ← <span class="jp-label">Ubah URL</span>
      </button>
      <button
        id="btn-start-download"
        type="button"
        :disabled="!selectedFormat"
        class="flex-[2] py-3 rounded-xl font-semibold text-sm text-white transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
        :class="[
          selectedFormat
            ? 'bg-accent hover:bg-accent-hover active:scale-[0.98] shadow-lg shadow-accent/20'
            : 'bg-muted/30',
        ]"
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
        <span class="jp-label">Mulai Download</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  videoInfo: { type: Object, default: null },
  selectedType: { type: String, default: "video" },
  selectedFormat: { type: Object, default: null },
});

defineEmits(["selectType", "selectFormat", "startDownload", "reset"]);

const tabs = [
  { value: "video", label: "Video", icon: "🎬 " },
  { value: "audio", label: "Audio", icon: "🎵 " },
];

const filteredFormats = computed(() => {
  if (!props.videoInfo?.formats) return [];
  return props.videoInfo.formats.filter((f) => f.type === props.selectedType);
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
