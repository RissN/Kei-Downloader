<template>
  <div class="glass rounded-2xl p-6 sm:p-8 animate-fade-in space-y-6">
    <!-- Heading -->
    <div class="text-center space-y-2">
      <p class="text-accent text-xs font-bold tracking-widest jp-label uppercase">
        Tempel Tautan
      </p>
      <h2 class="text-2xl sm:text-3xl font-extrabold text-text">
        Download YouTube Video
      </h2>
      <p class="text-muted text-sm">Paste link YouTube di bawah ini</p>
    </div>

    <!-- Input form -->
    <form @submit.prevent="onSubmit" class="space-y-4">
      <div class="relative">
        <input
          id="url-input"
          ref="inputRef"
          v-model="url"
          type="url"
          placeholder="https://www.youtube.com/watch?v=..."
          class="w-full px-4 py-3.5 pr-10 rounded-xl text-text placeholder-muted/40 text-sm outline-none glass-input"
          :class="[
            validationError
              ? '!border-danger focus:!border-danger !shadow-danger/10'
              : '',
          ]"
          @paste="onPaste"
          @input="onInput"
        />
        <!-- Clear button -->
        <button
          v-if="url"
          type="button"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-muted/60 hover:text-accent transition-colors cursor-pointer"
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
        class="text-danger text-xs flex items-center gap-1.5"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-3.5 h-3.5 shrink-0"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
            clip-rule="evenodd"
          />
        </svg>
        {{ validationError }}
      </p>

      <!-- API error -->
      <div
        v-if="errorMessage"
        class="p-3 bg-danger/8 border border-danger/20 rounded-xl text-danger text-sm flex items-start gap-2"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-5 h-5 shrink-0 mt-0.5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clip-rule="evenodd"
          />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <!-- Submit button -->
      <button
        id="btn-fetch-info"
        type="submit"
        :disabled="!url || !!validationError || isLoading"
        class="w-full py-3.5 rounded-xl font-semibold text-sm text-white transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
        :class="[
          !url || !!validationError || isLoading
            ? 'bg-muted/30'
            : 'bg-accent hover:bg-accent-hover active:scale-[0.98] shadow-lg shadow-accent/20',
        ]"
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
          {{ isLoading ? "Mengambil Info..." : "Ambil Info" }}
        </span>
      </button>
    </form>
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
