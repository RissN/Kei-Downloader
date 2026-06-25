<template>
  <div class="animate-fade-in space-y-6">
    <!-- Video preview -->
    <div class="bg-surface border border-edge rounded-2xl overflow-hidden">
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
          class="absolute bottom-2 right-2 bg-black/80 text-white text-xs font-medium px-2 py-0.5 rounded"
        >
          {{ formatDuration(videoInfo.duration) }}
        </span>
      </div>
      <div class="p-4">
        <h3 class="text-white font-bold text-base leading-snug line-clamp-2">
          {{ videoInfo?.title }}
        </h3>
      </div>
    </div>

    <!-- Tab switcher -->
    <div class="flex bg-surface border border-edge rounded-xl p-1 gap-1">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :id="`tab-${tab.value}`"
        class="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 cursor-pointer"
        :class="[
          selectedType === tab.value
            ? 'bg-accent text-white shadow-lg shadow-accent/20'
            : 'text-muted hover:text-white hover:bg-surface-hover',
        ]"
        @click="$emit('selectType', tab.value)"
      >
        {{ tab.icon }} {{ tab.label }}
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
        class="relative p-4 rounded-xl border text-left transition-all duration-200 cursor-pointer"
        :class="[
          selectedFormat?.format_id === fmt.format_id
            ? 'border-accent bg-accent/10 ring-1 ring-accent/30'
            : 'border-edge bg-surface hover:border-edge-light hover:bg-surface-hover',
        ]"
        @click="$emit('selectFormat', fmt)"
      >
        <!-- Badge terbaik -->
        <span
          v-if="idx === 0"
          class="absolute -top-2 right-3 bg-accent text-white text-[10px] font-bold px-2 py-0.5 rounded-full"
        >
          Terbaik
        </span>

        <div class="space-y-1.5">
          <span class="text-white font-bold text-base">
            {{ fmt.quality_label }}
          </span>
          <div class="flex items-center gap-2 text-xs text-muted">
            <span
              class="px-1.5 py-0.5 bg-edge rounded text-[10px] font-semibold uppercase"
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
        class="flex-1 py-3 rounded-xl border border-edge text-muted hover:text-white hover:border-edge-light font-medium text-sm transition-all duration-200 cursor-pointer"
        @click="$emit('reset')"
      >
        ← Ganti URL
      </button>
      <button
        id="btn-start-download"
        type="button"
        :disabled="!selectedFormat"
        class="flex-[2] py-3 rounded-xl font-semibold text-sm text-white transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        :class="[
          selectedFormat
            ? 'bg-accent hover:bg-accent-hover active:scale-[0.98] cursor-pointer'
            : 'bg-edge',
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
        Mulai Download
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
  { value: "video", label: "Video", icon: "🎬" },
  { value: "audio", label: "Audio", icon: "🎵" },
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
