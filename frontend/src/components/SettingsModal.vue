<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="$emit('close')"></div>

    <!-- Modal Content -->
    <div class="relative w-full max-w-md glass-strong rounded-2xl p-6 sm:p-8 space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-text jp-label">Pengaturan</h2>
        <button @click="$emit('close')" class="text-muted hover:text-text cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-5">
        <!-- Default Tab -->
        <div class="space-y-2">
          <label class="text-sm font-semibold text-text jp-label block">Tipe Default</label>
          <div class="flex glass-subtle rounded-xl p-1 gap-1">
            <button
              v-for="type in ['video', 'audio']"
              :key="type"
              class="flex-1 py-2 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer capitalize"
              :class="[
                settings.defaultType === type
                  ? 'bg-accent text-white shadow-md'
                  : 'text-muted hover:text-text hover:bg-white/30',
              ]"
              @click="settings.defaultType = type"
            >
              {{ type }}
            </button>
          </div>
        </div>

        <!-- Subtitles -->
        <div class="flex items-center justify-between glass-card p-4 rounded-xl">
          <div>
            <p class="text-sm font-semibold text-text jp-label">Embed Subtitle</p>
            <p class="text-xs text-muted mt-0.5">Otomatis download dan tanamkan subtitle (ID/EN) jika tersedia.</p>
          </div>
          <button
            class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors cursor-pointer"
            :class="settings.includeSubtitles ? 'bg-accent' : 'bg-muted/30'"
            @click="settings.includeSubtitles = !settings.includeSubtitles"
          >
            <span
              class="inline-block h-5 w-5 transform rounded-full bg-white shadow-sm transition-transform"
              :class="settings.includeSubtitles ? 'translate-x-5' : 'translate-x-[2px]'"
            />
          </button>
        </div>
      </div>

      <button
        class="w-full py-3 bg-text text-white rounded-xl font-semibold text-sm transition-all hover:opacity-90 active:scale-[0.98] cursor-pointer jp-label"
        @click="$emit('close')"
      >
        Tutup
      </button>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from "../stores/settingsStore";

defineEmits(["close"]);
const settings = useSettingsStore();
</script>
