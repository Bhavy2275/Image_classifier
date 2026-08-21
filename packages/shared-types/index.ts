/**
 * Shared TypeScript types for VisionAI.
 *
 * Re-exports all types from the web app's lib/types.ts.
 * Import these in any package in the monorepo that needs them.
 */

export type {
  TopKClass,
  PredictionResult,
  PredictionHistoryItem,
  HistoryResponse,
  BatchJobStatus,
  BatchJobItem,
  BatchJobResponse,
  BatchStatusResponse,
} from "../../apps/web/lib/types";
