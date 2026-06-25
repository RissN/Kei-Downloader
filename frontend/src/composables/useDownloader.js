/**
 * Composable — orchestrator that combines store + SSE + download trigger.
 */

import { storeToRefs } from "pinia";
import { useDownloadStore } from "../stores/downloadStore";
import { useSettingsStore } from "../stores/settingsStore";
import { useSSE } from "./useSSE";
import { buildDownloadUrl } from "../services/api";

export function useDownloader() {
  const store = useDownloadStore();
  const settings = useSettingsStore();

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
    // Auto-select type based on settings
    store.selectedType = settings.defaultType;
    store._autoSelectBest();
  }

  /** Mulai download tunggal: open SSE → trigger browser download. */
  function handleStartDownload() {
    if (!selectedFormat.value || !videoInfo.value) return;

    store.startDownload();

    const taskId = store.taskId;
    const downloadUrl = buildDownloadUrl(
      url.value,
      selectedFormat.value.format_id,
      taskId,
      settings.includeSubtitles
    );

    _triggerDownloadAndTrack(taskId, downloadUrl, videoInfo.value, selectedFormat.value);
  }

  /**
   * Mulai download berurutan untuk playlist.
   * @param {{ urls: string[], type: string }} data
   */
  async function handleStartBatchDownload({ urls, type }) {
    if (!urls.length) return;
    
    // Set status
    store.status = "downloading";
    store.selectedType = type;
    
    let currentIdx = 0;

    const runNext = async () => {
      if (currentIdx >= urls.length) {
        store.status = "done";
        return;
      }
      
      const currentUrl = urls[currentIdx];
      
      // Update progress logic here: Instead of simple 0-100, we could track overall, 
      // but for simplicity let's just show progress for the current file and reset it for the next.
      store.progress = 0;
      
      // 1. Fetch info for this specific url
      try {
        const response = await fetch("/api/info", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: currentUrl }),
        });
        
        if (!response.ok) throw new Error("Failed fetch");
        const info = await response.json();
        
        // Pick best format
        const formats = info.formats.filter(f => f.type === type);
        const bestFormat = formats[0]; // First is best based on how we parse
        
        if (!bestFormat) {
            throw new Error("Format not found");
        }
        
        // Set temp info for UI
        store.videoInfo = info;
        store.selectedFormat = bestFormat;
        
        const taskId = crypto.randomUUID();
        const downloadUrl = buildDownloadUrl(
          currentUrl,
          bestFormat.format_id,
          taskId,
          settings.includeSubtitles
        );
        
        // Track this individual download via SSE, wrapped in a Promise
        await new Promise((resolve) => {
           connect(taskId, {
              onProgress(pct) {
                store.progress = pct;
              },
              onDone() {
                store.progress = 100;
                store.addToHistory({
                  title: info.title,
                  thumbnail: info.thumbnail,
                  type: type,
                  quality: bestFormat.quality_label,
                  timestamp: Date.now(),
                });
                disconnect();
                resolve();
              },
              onError(msg) {
                console.error("Download failed:", msg);
                disconnect();
                resolve(); // Continue to next even if error
              }
           });
           
           // Trigger download
           const a = document.createElement("a");
           a.href = downloadUrl;
           a.download = "";
           a.style.display = "none";
           document.body.appendChild(a);
           a.click();
           document.body.removeChild(a);
        });

      } catch (err) {
        console.error("Batch item error", err);
      }
      
      currentIdx++;
      runNext();
    };

    runNext();
  }

  function _triggerDownloadAndTrack(taskId, downloadUrl, info, format) {
    connect(taskId, {
      onProgress(pct) {
        store.progress = pct;
      },
      onDone() {
        store.progress = 100;
        store.status = "done";
        store.addToHistory({
          title: info?.title ?? "",
          thumbnail: info?.thumbnail ?? "",
          type: format?.type ?? "video",
          quality: format?.quality_label ?? "",
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
    handleStartBatchDownload,
    handleReset,
    selectType,
    selectFormat,
  };
}
