/**
 * Typed API client for the FastAPI backend.
 * Automatically attaches the Supabase JWT from localStorage.
 */
import type {
  BatchJobResponse,
  BatchStatusResponse,
  HistoryResponse,
  PredictionResult,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function getAuthHeaders(): Promise<HeadersInit> {
  // Import lazily to avoid SSR issues
  const { supabase } = await import("./supabase-client");
  const {
    data: { session },
  } = await supabase.auth.getSession();
  const token = session?.access_token;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const authHeaders = await getAuthHeaders();
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      ...authHeaders,
      ...(options.headers ?? {}),
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail ?? `API error ${res.status}`);
  }

  return res.json() as Promise<T>;
}

// ── Predict ───────────────────────────────────────────────────

export async function predictImage(
  file: File,
  includeHeatmap = true
): Promise<PredictionResult> {
  const form = new FormData();
  form.append("image", file);
  form.append("include_heatmap", String(includeHeatmap));

  return apiFetch<PredictionResult>("/predict", {
    method: "POST",
    body: form,
  });
}

// ── Batch ─────────────────────────────────────────────────────

export async function submitBatchJob(
  files: File[]
): Promise<BatchJobResponse> {
  const form = new FormData();
  files.forEach((f) => form.append("images", f));

  return apiFetch<BatchJobResponse>("/batch/predict", {
    method: "POST",
    body: form,
  });
}

export async function getBatchStatus(
  jobId: string
): Promise<BatchStatusResponse> {
  return apiFetch<BatchStatusResponse>(`/batch/status/${jobId}`);
}

// ── History ───────────────────────────────────────────────────

export async function getHistory(
  page = 1,
  pageSize = 20
): Promise<HistoryResponse> {
  return apiFetch<HistoryResponse>(
    `/history?page=${page}&page_size=${pageSize}`
  );
}
