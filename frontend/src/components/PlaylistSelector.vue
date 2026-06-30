<template>
  <div class="card-kawaii p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Header -->
    <div class="text-center space-y-2">
      <h2 class="text-xl sm:text-2xl font-extrabold text-gradient jp-display">
        Playlist Ditemukan!
      </h2>
      <h3 class="text-base font-bold truncate" style="color: var(--color-text);">
        {{ videoInfo?.title }}
      </h3>
      <p class="text-sm" style="color: var(--color-muted);">{{ items.length }} Video Tersedia</p>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-between p-3 rounded-full" style="background: var(--color-bg-surface2); border: 1px solid var(--color-border);">
      <button
        class="text-sm font-bold px-4 py-2 rounded-full transition-all cursor-pointer"
        style="color: var(--color-text);"
        @mouseenter="$event.target.style.background = 'var(--color-accent-soft)'"
        @mouseleave="$event.target.style.background = 'transparent'"
        @click="toggleAll"
      >
        {{ allSelected ? "Batal Pilih" : "Pilih Semua" }}
      </button>
      <div class="text-sm font-bold px-4" style="color: var(--color-accent);">
        {{ selectedCount }} Terpilih
      </div>
    </div>

    <!-- List -->
    <div class="space-y-2 max-h-[350px] overflow-y-auto pr-2">
      <label
        v-for="(item, idx) in items"
        :key="idx"
        class="flex items-center gap-3 p-3 rounded-2xl cursor-pointer transition-all"
        style="background: var(--color-bg-surface); border: 1px solid var(--color-border);"
        @mouseenter="$event.currentTarget.style.background = 'var(--color-bg-surface2)'"
        @mouseleave="$event.currentTarget.style.background = 'var(--color-bg-surface)'"
      >
        <div class="shrink-0">
          <input
            type="checkbox"
            v-model="item.selected"
            class="w-5 h-5 rounded cursor-pointer accent-[var(--color-accent)]"
          />
        </div>
        <!-- Thumbnail -->
        <img
          v-if="item.thumbnail"
          :src="item.thumbnail"
          :alt="item.title"
          class="w-[60px] h-[40px] object-cover rounded-lg shrink-0"
        />
        <div
          v-else
          class="w-[60px] h-[40px] rounded-lg shrink-0 flex items-center justify-center text-xs"
          style="background: var(--color-bg-surface2); color: var(--color-muted);"
        >
          ▶
        </div>
        <!-- Title -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium line-clamp-2 leading-snug" style="color: var(--color-text);">
            {{ item.title }}
          </p>
        </div>
      </label>
    </div>

    <!-- Global Format selector for Playlist -->
    <div class="p-4 rounded-2xl space-y-3" style="background: var(--color-bg-surface2); border: 1px solid var(--color-border);">
      <p class="text-sm font-bold jp-label" style="color: var(--color-text);">Pilih Format:</p>
      <div class="tab-kawaii">
        <button
          v-for="type in ['video', 'audio']"
          :key="type"
          :class="[
            selectedType === type ? 'tab-active' : '',
          ]"
          @click="selectedType = type"
        >
          {{ type === 'video' ? 'Video (Terbaik)' : 'Audio (Terbaik)' }}
        </button>
      </div>
    </div>

    <!-- Buttons -->
    <div class="flex gap-3 mt-4">
      <button
        type="button"
        class="flex-1 btn-ghost"
        @click="$emit('reset')"
      >
        <span class="jp-label">Batal</span>
      </button>
      <button
        type="button"
        :disabled="selectedCount === 0"
        class="flex-[2] btn-primary"
        :style="selectedCount === 0 ? 'background: var(--color-text-muted); box-shadow: none;' : ''"
        @click="startDownload"
      >
        <span class="jp-label">Download ({{ selectedCount }})</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useSettingsStore } from "../stores/settingsStore";

const props = defineProps({
  videoInfo: { type: Object, default: null },
});

const emit = defineEmits(["startBatchDownload", "reset"]);
const settings = useSettingsStore();

const items = ref([]);
const selectedType = ref(settings.defaultType);

onMounted(() => {
  if (props.videoInfo?.playlist_items) {
    items.value = props.videoInfo.playlist_items.map((it) => ({
      ...it,
      selected: true,
    }));
  }
});

const selectedCount = computed(() => items.value.filter((i) => i.selected).length);
const allSelected = computed(() => selectedCount.value === items.value.length && items.value.length > 0);

function toggleAll() {
  const targetState = !allSelected.value;
  items.value.forEach((i) => (i.selected = targetState));
}

function startDownload() {
  const selectedUrls = items.value.filter((i) => i.selected).map((i) => i.url);
  emit("startBatchDownload", {
    urls: selectedUrls,
    type: selectedType.value,
    // Kita gunakan resolusi tertinggi secara otomatis untuk playlist
  });
}
</script>
