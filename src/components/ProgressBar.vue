<template>
  <div class="card p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Video info -->
    <div class="flex items-center gap-4 p-4 rounded-2xl" style="background: var(--color-bg-surface2); border: 1px solid var(--color-border);">
      <img
        v-if="videoInfo?.thumbnail"
        :src="videoInfo.thumbnail"
        :alt="videoInfo?.title"
        class="w-20 h-[60px] object-cover rounded-xl shrink-0"
      />
      <div class="min-w-0 flex-1">
        <h3 class="font-bold text-sm truncate" style="color: var(--color-text);">
          {{ videoInfo?.title }}
        </h3>
        <p class="text-xs mt-1" style="color: var(--color-muted);">
          {{ selectedFormat?.quality_label }} ·
          {{ selectedFormat?.ext?.toUpperCase() }}
        </p>
      </div>
    </div>

    <!-- Progress bar -->
    <div class="space-y-3">
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{
            width: `${progress}%`,
            background: progress >= 100
              ? 'var(--color-success)'
              : 'linear-gradient(135deg, var(--color-accent), var(--color-purple))',
          }"
        ></div>
        <span
          class="progress-label drop-shadow-sm"
          :style="{
            color: progress > 45 ? '#fff' : 'var(--color-text)',
          }"
        >
          {{ Math.round(progress) }}%
        </span>
      </div>

      <!-- Status text -->
      <p class="text-center text-sm" style="color: var(--color-muted);">
        <span v-if="progress < 90" class="text-label">
          Mengunduh...
          <span class="font-bold" style="color: var(--color-accent);">{{ Math.round(progress) }}%</span>
        </span>
        <span v-else-if="progress < 99" class="text-label">
          Menyimpan file...
          <span class="font-bold" style="color: var(--color-accent);">{{ Math.round(progress) }}%</span>
        </span>
        <span v-else-if="progress < 100" class="text-label">
          Memproses...
        </span>
        <span v-else class="font-bold text-display" style="color: var(--color-accent);">
          Selesai!
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
