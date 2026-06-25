<template>
  <div class="animate-fade-in space-y-6">
    <!-- Video info -->
    <div class="flex items-center gap-4 p-4 bg-surface rounded-2xl border border-edge">
      <img
        v-if="videoInfo?.thumbnail"
        :src="videoInfo.thumbnail"
        :alt="videoInfo?.title"
        class="w-20 h-[60px] object-cover rounded-lg shrink-0"
      />
      <div class="min-w-0 flex-1">
        <h3 class="text-white font-semibold text-sm truncate">
          {{ videoInfo?.title }}
        </h3>
        <p class="text-muted text-xs mt-1">
          {{ selectedFormat?.quality_label }} ·
          {{ selectedFormat?.ext?.toUpperCase() }}
        </p>
      </div>
    </div>

    <!-- Progress bar -->
    <div class="space-y-3">
      <div
        class="relative w-full h-10 bg-surface rounded-full overflow-hidden border border-edge"
      >
        <div
          class="h-full rounded-full transition-all duration-500 ease-out"
          :class="[
            progress < 100
              ? 'bg-gradient-to-r from-accent to-accent-hover animate-pulse-glow'
              : 'bg-success',
          ]"
          :style="{ width: `${progress}%` }"
        ></div>
        <span
          class="absolute inset-0 flex items-center justify-center text-sm font-bold text-white drop-shadow-md"
        >
          {{ Math.round(progress) }}%
        </span>
      </div>

      <!-- Status text -->
      <p class="text-center text-muted text-sm">
        <span v-if="progress < 99"> Mengunduh... {{ Math.round(progress) }}% </span>
        <span v-else-if="progress < 100"> Memproses file... </span>
        <span v-else class="text-success font-semibold">
          ✓ Selesai! File sedang disimpan...
        </span>
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  /** @type {number} Progress 0–100 */
  progress: { type: Number, default: 0 },
  /** @type {{ title: string, thumbnail: string } | null} */
  videoInfo: { type: Object, default: null },
  /** @type {{ quality_label: string, ext: string } | null} */
  selectedFormat: { type: Object, default: null },
});
</script>
