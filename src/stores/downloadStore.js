/**
 * Pinia store — global download state management.
 */

import { defineStore } from "pinia";
import { fetchVideoInfo } from "../services/api";

/**
 * Load history from localStorage.
 * @returns {Array<{title: string, thumbnail: string, type: string, quality: string, timestamp: number}>}
 */
function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem("downloadHistory") || "[]");
  } catch {
    return [];
  }
}

export const useDownloadStore = defineStore("download", {
  state: () => ({
    /** @type {string} */
    url: "",
    /** @type {{ title: string, thumbnail: string, duration: number, formats: Array } | null} */
    videoInfo: null,
    /** @type {{ format_id: string, ext: string, resolution: string, filesize_approx: number|null, quality_label: string, type: string } | null} */
    selectedFormat: null,
    /** @type {'video' | 'audio'} */
    selectedType: "video",
    /** @type {string} */
    taskId: "",
    /** @type {'idle' | 'loading' | 'selecting' | 'downloading' | 'done' | 'error'} */
    status: "idle",
    /** @type {number} 0–100 */
    progress: 0,
    /** @type {string} */
    errorMessage: "",
    /** @type {Array<{title: string, thumbnail: string, type: string, quality: string, timestamp: number}>} */
    history: loadHistory(),
  }),

  actions: {
    /** Fetch video info dari backend, lalu set status ke 'selecting'. */
    async fetchInfo() {
      this.status = "loading";
      this.errorMessage = "";
      try {
        this.videoInfo = await fetchVideoInfo(this.url);
        this.status = "selecting";
        // Auto-select format terbaik sesuai tab aktif
        this._autoSelectBest();
      } catch (/** @type {Error} */ err) {
        this.status = "error";
        this.errorMessage = err.message;
      }
    },

    /** Mulai download — generate task ID, set status. */
    startDownload() {
      this.taskId = crypto.randomUUID();
      this.status = "downloading";
      this.progress = 0;
    },

    /** Reset ke state awal. */
    reset() {
      this.url = "";
      this.videoInfo = null;
      this.selectedFormat = null;
      this.selectedType = "video";
      this.taskId = "";
      this.status = "idle";
      this.progress = 0;
      this.errorMessage = "";
    },

    /**
     * Tambah item ke history dan persist ke localStorage.
     * @param {{ title: string, thumbnail: string, type: string, quality: string, timestamp: number }} item
     */
    addToHistory(item) {
      this.history.unshift(item);
      // Batasi 30 item
      if (this.history.length > 30) {
        this.history = this.history.slice(0, 30);
      }
      localStorage.setItem("downloadHistory", JSON.stringify(this.history));
    },

    /** Hapus semua history. */
    clearHistory() {
      this.history = [];
      localStorage.removeItem("downloadHistory");
    },

    /** Auto-select format kualitas tertinggi untuk tipe yang aktif. */
    _autoSelectBest() {
      if (!this.videoInfo) return;
      const formats = this.videoInfo.formats.filter(
        (/** @type {{ type: string }} */ f) => f.type === this.selectedType,
      );
      this.selectedFormat = formats.length > 0 ? formats[0] : null;
    },
  },
});
