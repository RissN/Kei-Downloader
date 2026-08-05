<template>
  <div class="card p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Video preview -->
    <div class="rounded-2xl overflow-hidden" style="border: 1.5px solid var(--color-border);">
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
          class="absolute bottom-2 right-2 text-white text-xs font-bold px-2.5 py-1 rounded-full"
          style="background: rgba(26, 54, 54, 0.8); backdrop-filter: blur(4px);"
        >
          {{ formatDuration(videoInfo.duration) }}
        </span>
      </div>
      <div class="p-4" style="background: var(--color-bg-surface);">
        <h3 class="font-bold text-base leading-snug line-clamp-2" style="color: var(--color-text);">
          {{ videoInfo?.title }}
        </h3>
      </div>
    </div>

    <!-- Section title -->
    <div class="text-center space-y-1">
      <h3 class="text-lg font-extrabold text-gradient text-display">Pilih Format</h3>
      <p class="text-xs" style="color: var(--color-muted);">Pilih Format</p>
    </div>

    <!-- Tab switcher -->
    <div class="tab-group">
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

    <!-- Format grid -->
    <div v-if="selectedType === 'audio'" class="flex justify-center -mt-2 mb-4 animate-fade-in">
      <div class="relative">
        <select
          v-model="selectedAudioCodec"
          class="appearance-none bg-transparent border border-[var(--color-border)] rounded-full px-4 py-1.5 pr-8 text-sm font-bold text-[var(--color-text)] outline-none focus:border-[var(--color-primary)] transition-colors cursor-pointer"
          style="background: var(--color-bg-surface);"
        >
          <option value="mp3">Format: MP3</option>
          <option value="opus">Format: OPUS</option>
        </select>
        <!-- Custom dropdown arrow -->
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3" style="color: var(--color-muted);">
          <svg class="w-4 h-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
        </div>
      </div>
    </div>

    <TransitionGroup
      name="format-list"
      tag="div"
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
        class="text-left transition-all duration-200 cursor-pointer"
        :class="[
          selectedFormat?.format_id === fmt.format_id
            ? 'format-card format-card-selected'
            : 'format-card',
        ]"
        :style="{ animationDelay: `${idx * 50}ms` }"
        @click="$emit('selectFormat', fmt)"
      >
        <!-- Best badge -->
        <span
          v-if="idx === 0"
          class="badge-best absolute -top-2 right-3"
        >
          Terbaik
        </span>

        <div class="space-y-1.5">
          <span class="font-bold text-base" style="color: var(--color-text);">
            {{ fmt.quality_label }}
          </span>
          <div class="flex items-center gap-2 text-xs" style="color: var(--color-muted);">
            <span
              class="px-1.5 py-0.5 rounded-full text-[10px] font-bold uppercase"
              style="background: var(--color-bg-surface2); color: var(--color-muted);"
            >
              .{{ fmt.ext }}
            </span>
            <span v-if="fmt.filesize_approx">
              ~{{ formatSize(fmt.filesize_approx) }}
            </span>
          </div>
        </div>
      </button>
    </TransitionGroup>

    <!-- Actions -->
    <div class="flex gap-3">
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
