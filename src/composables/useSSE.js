/**
 * Composable — SSE connection manager.
 */

import { ref } from "vue";
import { createProgressSSE } from "../services/api";

export function useSSE() {
  /** @type {import('vue').Ref<EventSource | null>} */
  const source = ref(null);

  /**
   * Open SSE connection for a task.
   * @param {string} taskId
   * @param {{ onProgress: (p: number) => void, onDone: () => void, onError: (msg: string) => void }} callbacks
   */
  function connect(taskId, { onProgress, onDone, onError }) {
    disconnect();
    source.value = createProgressSSE(taskId, onProgress, onDone, onError);
  }

  /** Close active SSE connection. */
  function disconnect() {
    if (source.value) {
      source.value.close();
      source.value = null;
    }
  }

  return { connect, disconnect };
}
