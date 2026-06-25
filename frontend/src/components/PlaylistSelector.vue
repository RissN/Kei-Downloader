<template>
  <div class="glass rounded-2xl p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Header -->
    <div class="text-center space-y-2">
      <p class="text-accent text-xs font-bold tracking-widest jp-label uppercase">
        PLAYLIST DITEMUKAN
      </p>
      <h2 class="text-xl sm:text-2xl font-bold text-text truncate">
        {{ videoInfo?.title }}
      </h2>
      <p class="text-muted text-sm">{{ items.length }} Video Tersedia</p>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-between glass-subtle p-2 rounded-xl">
      <button
        class="text-sm font-semibold text-text px-4 py-2 hover:bg-white/30 rounded-lg transition-colors cursor-pointer"
        @click="toggleAll"
      >
        {{ allSelected ? "Batal Pilih Semua" : "Pilih Semua" }}
      </button>
      <div class="text-sm text-muted font-medium px-4">
        {{ selectedCount }} Terpilih
      </div>
    </div>

    <!-- List -->
    <div class="space-y-2 max-h-[350px] overflow-y-auto pr-2">
      <label
        v-for="(item, idx) in items"
        :key="idx"
        class="flex items-center gap-3 p-3 glass-card rounded-xl cursor-pointer hover:bg-white/40 transition-colors"
      >
        <div class="shrink-0">
          <input
            type="checkbox"
            v-model="item.selected"
            class="w-5 h-5 text-accent rounded border-white/40 bg-white/20 focus:ring-accent/50 cursor-pointer"
          />
        </div>
        <!-- Thumbnail -->
        <img
          v-if="item.thumbnail"
          :src="item.thumbnail"
          :alt="item.title"
          class="w-[60px] h-[40px] object-cover rounded-md shrink-0"
        />
        <div
          v-else
          class="w-[60px] h-[40px] bg-black/5 rounded-md shrink-0 flex items-center justify-center text-muted text-xs"
        >
          ▶
        </div>
        <!-- Title -->
        <div class="flex-1 min-w-0">
          <p class="text-text text-sm font-medium line-clamp-2 leading-snug">
            {{ item.title }}
          </p>
        </div>
      </label>
    </div>

    <!-- Global Format selector for Playlist -->
    <div class="glass-subtle p-4 rounded-xl space-y-3">
      <p class="text-sm font-semibold text-text jp-label">Pilih Format Download:</p>
      <div class="flex gap-2">
        <button
          v-for="type in ['video', 'audio']"
          :key="type"
          class="flex-1 py-2 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer capitalize"
          :class="[
            selectedType === type
              ? 'bg-accent text-white shadow-md'
              : 'text-muted hover:text-text hover:bg-white/30 bg-white/10',
          ]"
          @click="selectedType = type"
        >
          {{ type }} (Terbaik)
        </button>
      </div>
    </div>

    <!-- Buttons -->
    <div class="flex gap-3 mt-4">
      <button
        type="button"
        class="flex-1 py-3 rounded-xl glass-subtle text-muted hover:text-text font-medium text-sm transition-all duration-200 cursor-pointer"
        @click="$emit('reset')"
      >
        Batal
      </button>
      <button
        type="button"
        :disabled="selectedCount === 0"
        class="flex-[2] py-3 rounded-xl font-semibold text-sm text-white transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
        :class="[
          selectedCount > 0
            ? 'bg-accent hover:bg-accent-hover shadow-lg shadow-accent/20 active:scale-[0.98]'
            : 'bg-muted/30',
        ]"
        @click="startDownload"
      >
        Mulai Download ({{ selectedCount }})
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
