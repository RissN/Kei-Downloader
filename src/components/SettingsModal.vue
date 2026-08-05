<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 backdrop-blur-sm" style="background: rgba(26, 54, 54, 0.3);" @click="$emit('close')"></div>

    <!-- Modal Content -->
    <div class="modal-card relative w-full max-w-md card p-6 sm:p-8 space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-extrabold text-gradient text-display">Pengaturan</h2>
        <button @click="$emit('close')" class="cursor-pointer rounded-full w-8 h-8 flex items-center justify-center transition-all" style="color: var(--color-muted);"
          @mouseenter="$event.target.style.color = 'var(--color-accent)'; $event.target.style.background = 'var(--color-bg-surface2)'"
          @mouseleave="$event.target.style.color = 'var(--color-muted)'; $event.target.style.background = 'transparent'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-5">
        <!-- Default Tab -->
        <div class="space-y-2">
          <label class="text-sm font-bold text-label block" style="color: var(--color-text);">Tipe Default</label>
          <div class="tab-group">
            <button
              v-for="type in ['video', 'audio']"
              :key="type"
              :class="[
                settings.defaultType === type ? 'tab-active' : '',
              ]"
              @click="settings.defaultType = type"
            >
              {{ type === 'video' ? 'Video' : 'Audio' }}
            </button>
          </div>
        </div>

        <!-- Subtitles -->
        <div class="flex items-center justify-between p-4 rounded-2xl" style="background: var(--color-bg-surface); border: 1px solid var(--color-border);">
          <div>
            <p class="text-sm font-bold text-label" style="color: var(--color-text);">Embed Subtitle</p>
            <p class="text-xs mt-0.5" style="color: var(--color-muted);">Otomatis download dan tanamkan subtitle (ID/EN) jika tersedia.</p>
          </div>
          <button
            class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors cursor-pointer"
            :style="{
              background: settings.includeSubtitles
                ? 'linear-gradient(135deg, var(--color-accent), var(--color-purple))'
                : 'var(--color-border)',
            }"
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
        class="w-full btn-primary"
        @click="$emit('close')"
      >
        <span class="text-label">Tutup</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from "../stores/settingsStore";

defineEmits(["close"]);
const settings = useSettingsStore();
</script>
