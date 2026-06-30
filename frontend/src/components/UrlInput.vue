<template>
  <div class="card-kawaii p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Heading -->
    <div class="text-center space-y-2">
      <h2 class="text-3xl sm:text-4xl font-extrabold text-gradient jp-display">
        Download Video
      </h2>
      <p class="text-sm" style="color: var(--color-muted);">
        Paste link YouTube di bawah ini
      </p>
    </div>

    <!-- Input form -->
    <form @submit.prevent="onSubmit" class="space-y-4">
      <div class="relative">
        <input
          id="url-input"
          ref="inputRef"
          v-model="url"
          type="url"
          placeholder="Masukkan URL YouTube di sini..."
          class="w-full px-4 py-3.5 pr-10 text-sm outline-none input-kawaii"
          :class="[
            validationError
              ? '!border-[var(--color-danger)] focus:!border-[var(--color-danger)]'
              : '',
          ]"
          :style="validationError ? 'box-shadow: 0 0 0 3px rgba(252, 165, 165, 0.2)' : ''"
          @paste="onPaste"
          @input="onInput"
        />
        <!-- Clear button -->
        <button
          v-if="url"
          type="button"
          class="absolute right-3 top-1/2 -translate-y-1/2 transition-colors cursor-pointer"
          style="color: var(--color-text-muted);"
          @mouseenter="$event.target.style.color = 'var(--color-accent)'"
          @mouseleave="$event.target.style.color = 'var(--color-text-muted)'"
          @click="clearInput"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>

      <!-- Validation error -->
      <p
        v-if="validationError"
        class="text-xs flex items-center gap-1.5"
        style="color: var(--color-danger);"
      >
        <span class="jp-display">(´；ω；｀)</span>
        {{ validationError }}
      </p>

      <!-- API error -->
      <div
        v-if="errorMessage"
        class="error-kawaii text-sm flex items-start gap-2"
      >
        <span class="jp-display text-base shrink-0">(´；ω；｀)</span>
        <span>{{ errorMessage }}</span>
      </div>

      <!-- Submit button -->
      <button
        id="btn-fetch-info"
        type="submit"
        :disabled="!url || !!validationError || isLoading"
        class="w-full btn-primary"
        :style="(!url || !!validationError || isLoading) ? 'background: var(--color-text-muted); box-shadow: none;' : ''"
      >
        <!-- Loading spinner -->
        <svg
          v-if="isLoading"
          class="w-5 h-5 animate-spin"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
          ></path>
        </svg>
        <span class="jp-label">
          {{ isLoading ? "Mengambil Info..." : "✦ Cek Video" }}
        </span>
      </button>
    </form>

    <!-- Hint -->
    <p class="hint-text text-center">
      Tips: YouTube, Shorts, dan Playlist didukung ✓
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useDownloader } from "../composables/useDownloader";

const { url, status, errorMessage, handleFetchInfo } = useDownloader();

const inputRef = ref(null);

const isLoading = computed(() => status.value === "loading");

/** @type {import('vue').Ref<string>} */
const validationError = ref("");

/** Pola URL YouTube yang valid */
const YT_REGEX =
  /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)/;

/** Validasi URL secara real-time. */
function validate(value) {
  if (!value) {
    validationError.value = "";
    return;
  }
  if (!YT_REGEX.test(value)) {
    validationError.value =
      "URL tidak valid. Gunakan format: youtube.com/watch?v=... atau youtu.be/...";
  } else {
    validationError.value = "";
  }
}

function onInput() {
  validate(url.value);
}

function onPaste() {
  setTimeout(() => {
    validate(url.value);
    if (!validationError.value && url.value) {
      handleFetchInfo();
    }
  }, 50);
}

function onSubmit() {
  validate(url.value);
  if (!validationError.value && url.value) {
    handleFetchInfo();
  }
}

function clearInput() {
  url.value = "";
  validationError.value = "";
  inputRef.value?.focus();
}

watch(status, (s) => {
  if (s === "idle") validationError.value = "";
});
</script>
