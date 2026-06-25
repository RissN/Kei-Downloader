/**
 * Composable — orchestrator that combines store + SSE + download trigger.
 */

import { storeToRefs } from "pinia";
import { useDownloadStore } from "../stores/downloadStore";
import { useSSE } from "./useSSE";
import { buildDownloadUrl } from "../services/api";

export function useDownloader() {
  const store = useDownloadStore();
  const {
    url,
    videoInfo,
    selectedType,
    selectedFormat,
    status,
    progress,
    history,
    errorMessage,
  } = storeToRefs(store);
  const { connect, disconnect } = useSSE();

  /** Fetch info video dari URL yang diinput user. */
  async function handleFetchInfo() {
    await store.fetchInfo();
  }

  /** Mulai download: open SSE → trigger browser download. */
  function handleStartDownload() {
    if (!selectedFormat.value || !videoInfo.value) return;

    store.startDownload();

    const taskId = store.taskId;
    const downloadUrl = buildDownloadUrl(
      url.value,
      selectedFormat.value.format_id,
      taskId,
    );

    // SSE untuk progress tracking
    connect(taskId, {
      onProgress(pct) {
        store.progress = pct;
      },
      onDone() {
        store.progress = 100;
        store.status = "done";
        store.addToHistory({
          title: videoInfo.value?.title ?? "",
          thumbnail: videoInfo.value?.thumbnail ?? "",
          type: selectedFormat.value?.type ?? "video",
          quality: selectedFormat.value?.quality_label ?? "",
          timestamp: Date.now(),
        });
        disconnect();
      },
      onError(msg) {
        store.status = "error";
        store.errorMessage = msg;
        disconnect();
      },
    });

    // Trigger browser download via hidden <a>
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "";
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  /** Reset state dan disconnect SSE. */
  function handleReset() {
    disconnect();
    store.reset();
  }

  /**
   * Ganti tipe format (video/audio) dan auto-select best.
   * @param {'video' | 'audio'} type
   */
  function selectType(type) {
    store.selectedType = type;
    store._autoSelectBest();
  }

  /**
   * Pilih format tertentu.
   * @param {{ format_id: string, ext: string, resolution: string, filesize_approx: number|null, quality_label: string, type: string }} format
   */
  function selectFormat(format) {
    store.selectedFormat = format;
  }

  return {
    url,
    videoInfo,
    selectedType,
    selectedFormat,
    status,
    progress,
    history,
    errorMessage,
    handleFetchInfo,
    handleStartDownload,
    handleReset,
    selectType,
    selectFormat,
  };
}
