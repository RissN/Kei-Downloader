/**
 * API service — helper functions for backend communication.
 */

/**
 * Fetch video info from the backend.
 * @param {string} url - YouTube URL
 * @returns {Promise<{title: string, thumbnail: string, duration: number, formats: Array}>}
 */
export async function fetchVideoInfo(url) {
  const response = await fetch("/api/info", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Terjadi kesalahan pada server" }));
    throw new Error(body.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Build the download URL with query params.
 * @param {string} url
 * @param {string} formatId
 * @param {string} taskId
 * @param {boolean} includeSubtitles
 * @returns {string}
 */
export function buildDownloadUrl(url, formatId, taskId, includeSubtitles = false) {
  const params = new URLSearchParams({
    url,
    format_id: formatId,
    task_id: taskId,
    include_subtitles: String(includeSubtitles),
  });
  return `/api/download?${params.toString()}`;
}

/**
 * Create an SSE connection for download progress tracking.
 * @param {string} taskId
 * @param {(progress: number) => void} onProgress
 * @param {() => void} onDone
 * @param {(error: string) => void} onError
 * @returns {EventSource}
 */
export function createProgressSSE(taskId, onProgress, onDone, onError) {
  const source = new EventSource(`/api/progress/${taskId}`);

  source.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.status === "done" || data.status === "streaming") {
        onDone();
        source.close();
      } else if (data.status === "error") {
        onError(data.error_msg || "Download gagal");
        source.close();
      } else {
        onProgress(data.progress || 0);
      }
    } catch {
      // Ignore JSON parse errors from malformed SSE data
    }
  };

  source.onerror = () => {
    onError("Koneksi ke server terputus");
    source.close();
  };

  return source;
}
