import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useSettingsStore = defineStore("settings", () => {
  // Default values
  const defaultType = ref(localStorage.getItem("setting_defaultType") || "video");
  const defaultQuality = ref(localStorage.getItem("setting_defaultQuality") || "best");
  const includeSubtitles = ref(localStorage.getItem("setting_includeSubtitles") === "true");

  // Watchers to persist in localStorage
  watch(defaultType, (val) => localStorage.setItem("setting_defaultType", val));
  watch(defaultQuality, (val) => localStorage.setItem("setting_defaultQuality", val));
  watch(includeSubtitles, (val) => localStorage.setItem("setting_includeSubtitles", String(val)));

  return {
    defaultType,
    defaultQuality,
    includeSubtitles,
  };
});
