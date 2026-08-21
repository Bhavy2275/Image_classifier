"use client";

import { useQuery } from "@tanstack/react-query";
import { getBatchStatus } from "@/lib/api-client";
import type { BatchStatusResponse } from "@/lib/types";

/**
 * Polls the batch job status every 2 seconds until the job is
 * completed or failed, then stops refetching.
 */
export function useBatchJob(jobId: string | null) {
  return useQuery<BatchStatusResponse, Error>({
    queryKey: ["batch-status", jobId],
    queryFn: () => getBatchStatus(jobId!),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (!data) return 2000;
      if (data.status === "completed" || data.status === "failed") return false;
      return 2000;
    },
    staleTime: 0,
  });
}
