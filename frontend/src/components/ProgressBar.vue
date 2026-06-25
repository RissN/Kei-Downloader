<template>
  <div class="glass rounded-2xl p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Video info -->
    <div class="flex items-center gap-4 p-4 glass-card rounded-xl">
      <img
        v-if="videoInfo?.thumbnail"
        :src="videoInfo.thumbnail"
        :alt="videoInfo?.title"
        class="w-20 h-[60px] object-cover rounded-lg shrink-0"
      />
      <div class="min-w-0 flex-1">
        <h3 class="text-text font-semibold text-sm truncate">
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
        class="relative w-full h-10 rounded-full overflow-hidden glass-subtle"
      >
        <div
          class="h-full rounded-full transition-all duration-500 ease-out"
          :class="[
            progress < 100
              ? 'bg-gradient-to-r from-accent to-sakura animate-pulse-glow'
              : 'bg-success',
          ]"
          :style="{ width: `${progress}%` }"
        ></div>
        <span
          class="absolute inset-0 flex items-center justify-center text-sm font-bold drop-shadow-sm"
          :class="progress > 45 ? 'text-white' : 'text-text'"
        >
          {{ Math.round(progress) }}%
        </span>
      </div>

      <!-- Status text -->
      <p class="text-center text-muted text-sm">
        <span v-if="progress < 99" class="jp-label">
          Mengunduh...
          <span class="text-text font-semibold">{{ Math.round(progress) }}%</span>
        </span>
        <span v-else-if="progress < 100" class="jp-label"> Memproses... </span>
        <span v-else class="text-success font-semibold jp-label">
          ✓ Selesai! Menyimpan file...
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
