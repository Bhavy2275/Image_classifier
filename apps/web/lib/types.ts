/**
 * Shared TypeScript interfaces mirroring the Pydantic backend schemas.
 * Keep in sync with apps/api/app/schemas/
 */

export interface TopKClass {
  rank: number;
  class_index: number;
  label: string;
  confidence: number;
}

export interface PredictionResult {
  prediction_id: string | null;
  image_url: string;
  top_classes: TopKClass[];
  heatmap_base64: string | null;
  processing_time_ms: number;
  created_at: string;
}

export interface PredictionHistoryItem {
  id: string;
  image_url: string;
  top_classes: TopKClass[];
  heatmap_url: string | null;
  batch_job_id: string | null;
  created_at: string;
}

export interface HistoryResponse {
  items: PredictionHistoryItem[];
  total: number;
  page: number;
  page_size: number;
}

// ── Batch ──────────────────────────────────────────────────────

export type BatchJobStatus = "pending" | "processing" | "completed" | "failed";

export interface BatchJobItem {
  filename: string;
  status: BatchJobStatus;
  prediction_id: string | null;
  image_url: string | null;
  top_classes: TopKClass[] | null;
  heatmap_base64: string | null;
  error: string | null;
}

export interface BatchJobResponse {
  job_id: string;
  total_images: number;
  status: BatchJobStatus;
  message: string;
}

export interface BatchStatusResponse {
  job_id: string;
  status: BatchJobStatus;
  total_images: number;
  completed_images: number;
  items: BatchJobItem[];
  created_at: string | null;
  updated_at: string | null;
}
