"use client";

import { useMutation } from "@tanstack/react-query";
import { predictImage } from "@/lib/api-client";
import type { PredictionResult } from "@/lib/types";

interface UseUploadImageOptions {
  onSuccess?: (data: PredictionResult) => void;
  onError?: (error: Error) => void;
}

export function useUploadImage(options: UseUploadImageOptions = {}) {
  return useMutation<PredictionResult, Error, { file: File; includeHeatmap?: boolean }>({
    mutationFn: ({ file, includeHeatmap = true }) =>
      predictImage(file, includeHeatmap),
    onSuccess: options.onSuccess,
    onError: options.onError,
  });
}
