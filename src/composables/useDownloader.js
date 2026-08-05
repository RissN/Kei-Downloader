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

  /** Mulai download tunggal: open SSE → fetch file → save to disk. */
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
      
      // Update progress: reset for each item
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
        
        // Track via SSE + fetch download, wrapped in a Promise
        await new Promise((resolve) => {
          // Phase 1: Track yt-dlp progress via SSE (server-side download: 0–90%)
          connect(taskId, {
            onProgress(pct) {
              // Map yt-dlp progress (0-99) to display range (0-90)
              store.progress = Math.min(pct * 0.9, 90);
            },
            onDone() {
              // yt-dlp finished — now fetch the file
              store.progress = 90;
              disconnect();
            },
            onError(msg) {
              console.error("SSE error:", msg);
              disconnect();
            }
          });

          // Phase 2: Fetch the file via HTTP (browser download: 90–100%)
          _fetchAndSaveFile(downloadUrl, info.title || "download")
            .then(() => {
              store.progress = 100;
              store.addToHistory({
                title: info.title,
                thumbnail: info.thumbnail,
                type: type,
                quality: bestFormat.quality_label,
                timestamp: Date.now(),
              });
              resolve();
            })
            .catch((err) => {
              console.error("Download fetch failed:", err);
              resolve(); // Continue to next even if error
            });
        });

      } catch (err) {
        console.error("Batch item error", err);
      }
      
      currentIdx++;
      runNext();
    };

    runNext();
  }

  /**
   * Download file via fetch, track transfer progress, lalu save ke disk.
   * @param {string} downloadUrl
   * @param {string} filename
   * @returns {Promise<void>}
   */
  async function _fetchAndSaveFile(downloadUrl, filename) {
    const response = await fetch(downloadUrl);

    if (!response.ok) {
      const errBody = await response.text().catch(() => "");
      throw new Error(`Download failed: HTTP ${response.status} - ${errBody}`);
    }

    // Extract filename from Content-Disposition header if available
    const disposition = response.headers.get("Content-Disposition");
    let savedFilename = filename;
    if (disposition) {
      // Try filename*=utf-8'' format first
      const utf8Match = disposition.match(/filename\*=utf-8''(.+)/i);
      if (utf8Match) {
        savedFilename = decodeURIComponent(utf8Match[1]);
      } else {
        const match = disposition.match(/filename="?([^";\n]+)"?/i);
        if (match) savedFilename = match[1];
      }
    }

    // Read the response as a stream to track transfer progress
    const contentLength = response.headers.get("Content-Length");
    const totalBytes = contentLength ? parseInt(contentLength, 10) : 0;

    const reader = response.body.getReader();
    const chunks = [];
    let receivedBytes = 0;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      receivedBytes += value.length;

      // Update progress: map transfer (0–100%) to display range (90–100%)
      if (totalBytes > 0) {
        const transferPct = (receivedBytes / totalBytes) * 100;
        store.progress = 90 + (transferPct / 100) * 10;
      }
    }

    // Combine chunks into a blob
    const blob = new Blob(chunks);
    const blobUrl = URL.createObjectURL(blob);

    // Trigger browser save dialog
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = savedFilename;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();

    // Cleanup
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(blobUrl);
    }, 1000);
  }

  function _triggerDownloadAndTrack(taskId, downloadUrl, info, format) {
    // Phase 1: Track yt-dlp server-side download progress via SSE (0–90%)
    connect(taskId, {
      onProgress(pct) {
        // Map yt-dlp progress (0-99) to display range (0-90)
        store.progress = Math.min(pct * 0.9, 90);
      },
      onDone() {
        // yt-dlp finished on server, file is being streamed
        store.progress = 90;
        disconnect();
      },
      onError(msg) {
        // SSE error doesn't mean download failed — fetch might still work
        console.warn("SSE tracking error:", msg);
        disconnect();
      },
    });

    // Phase 2: Fetch file and track transfer progress (90–100%)
    _fetchAndSaveFile(downloadUrl, info?.title || "download")
      .then(() => {
        store.progress = 100;
        store.status = "done";
        store.addToHistory({
          title: info?.title ?? "",
          thumbnail: info?.thumbnail ?? "",
          type: format?.type ?? "video",
          quality: format?.quality_label ?? "",
          timestamp: Date.now(),
        });
      })
      .catch((err) => {
        store.status = "error";
        store.errorMessage = err.message || "Download gagal";
        disconnect();
      });
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
