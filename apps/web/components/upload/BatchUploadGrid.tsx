"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";
import { clsx } from "clsx";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { useBatchJob } from "@/hooks/useBatchJob";
import { submitBatchJob } from "@/lib/api-client";
import type { BatchJobItem, BatchJobStatus } from "@/lib/types";

interface LocalFile {
  file: File;
  preview: string;
}

const ACCEPTED = {
  "image/jpeg": [".jpg", ".jpeg"],
  "image/png": [".png"],
  "image/webp": [".webp"],
};

function statusBadgeVariant(status: BatchJobStatus) {
  switch (status) {
    case "completed": return "success";
    case "failed": return "danger";
    case "processing": return "info";
    default: return "default";
  }
}

export function BatchUploadGrid() {
  const [files, setFiles] = useState<LocalFile[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const { data: jobData } = useBatchJob(jobId);

  const onDrop = useCallback((accepted: File[]) => {
    const remaining = 20 - files.length;
    const toAdd = accepted.slice(0, remaining).map((f) => ({
      file: f,
      preview: URL.createObjectURL(f),
    }));
    setFiles((prev) => [...prev, ...toAdd]);
  }, [files.length]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED,
    maxSize: 10 * 1024 * 1024,
    multiple: true,
    disabled: !!jobId || submitting,
  });

  const removeFile = (idx: number) => {
    setFiles((prev) => {
      URL.revokeObjectURL(prev[idx].preview);
      return prev.filter((_, i) => i !== idx);
    });
  };

  const handleSubmit = async () => {
    if (files.length === 0) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      const response = await submitBatchJob(files.map((f) => f.file));
      setJobId(response.job_id);
    } catch (err) {
      setSubmitError((err as Error).message);
    } finally {
      setSubmitting(false);
    }
  };

  const getItemStatus = (idx: number): BatchJobItem | null => {
    return jobData?.items?.[idx] ?? null;
  };

  return (
    <div className="space-y-6">
      {/* Drop zone */}
      {!jobId && (
        <div
          id="dropzone-batch"
          {...getRootProps()}
          className={clsx(
            "rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-300",
            isDragActive
              ? "border-accent-cyan/60 bg-accent-cyan/5 glow-border-cyan"
              : "border-white/10 hover:border-accent-cyan/40 hover:bg-white/[0.02]"
          )}
        >
          <input {...getInputProps()} id="batch-dropzone-input" />
          <div className="text-4xl mb-3">📁</div>
          <p className="text-white font-medium mb-1">
            {isDragActive ? "Drop images here!" : "Drag & drop up to 20 images"}
          </p>
          <p className="text-slate-500 text-sm">
            {files.length > 0
              ? `${files.length}/20 selected — drop more or click to add`
              : "JPEG, PNG, WebP accepted"}
          </p>
        </div>
      )}

      {/* File grid */}
      {files.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {files.map((lf, idx) => {
            const item = getItemStatus(idx);
            return (
              <div
                key={idx}
                className="glass rounded-2xl overflow-hidden group relative"
              >
                <div className="relative aspect-square bg-void-800">
                  <Image
                    src={lf.preview}
                    alt={lf.file.name}
                    fill
                    className="object-cover"
                    unoptimized
                  />
                  {/* Remove button */}
                  {!jobId && (
                    <button
                      id={`remove-file-${idx}`}
                      onClick={() => removeFile(idx)}
                      className="absolute top-2 right-2 w-6 h-6 bg-red-500 rounded-full text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center font-bold"
                    >
                      ×
                    </button>
                  )}
                  {/* Status overlay */}
                  {item && (
                    <div className="absolute inset-0 flex items-center justify-center bg-void-950/60">
                      {item.status === "processing" || item.status === "pending" ? (
                        <Spinner size="md" />
                      ) : item.status === "completed" ? (
                        <span className="text-2xl">✅</span>
                      ) : item.status === "failed" ? (
                        <span className="text-2xl">❌</span>
                      ) : null}
                    </div>
                  )}
                </div>
                <div className="p-2">
                  <p className="text-white text-xs truncate">{lf.file.name}</p>
                  {item ? (
                    <Badge variant={statusBadgeVariant(item.status)} className="mt-1">
                      {item.status}
                    </Badge>
                  ) : (
                    <p className="text-slate-500 text-xs mt-0.5">
                      {(lf.file.size / 1024).toFixed(0)} KB
                    </p>
                  )}
                  {item?.top_classes?.[0] && (
                    <p className="text-accent-green text-xs mt-1 truncate font-medium">
                      {item.top_classes[0].label} ({Math.round(item.top_classes[0].confidence * 100)}%)
                    </p>
                  )}
                  {item?.error && (
                    <p className="text-red-400 text-xs mt-1 truncate">{item.error}</p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Controls */}
      {!jobId && files.length > 0 && (
        <div className="flex items-center gap-4">
          <Button
            id="batch-submit"
            variant="primary"
            size="lg"
            isLoading={submitting}
            onClick={handleSubmit}
          >
            Classify {files.length} image{files.length !== 1 ? "s" : ""}
          </Button>
          <Button
            variant="ghost"
            onClick={() => { setFiles([]); setSubmitError(null); }}
          >
            Clear all
          </Button>
        </div>
      )}

      {submitError && (
        <div className="glass rounded-2xl p-4 border border-red-500/30 text-red-400 text-sm">
          ❌ {submitError}
        </div>
      )}

      {/* Job status summary */}
      {jobData && (
        <div className="glass rounded-2xl p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-white font-medium">Batch Job</span>
            <Badge variant={statusBadgeVariant(jobData.status)}>{jobData.status}</Badge>
          </div>
          {/* Progress bar */}
          <div className="w-full bg-white/5 rounded-full h-2 mb-3">
            <div
              className="bg-brand-500 h-2 rounded-full transition-all duration-500"
              style={{
                width: `${jobData.total_images > 0
                  ? (jobData.completed_images / jobData.total_images) * 100
                  : 0}%`,
              }}
            />
          </div>
          <p className="text-slate-400 text-sm">
            {jobData.completed_images}/{jobData.total_images} images processed
          </p>
          {jobData.status === "completed" && (
            <Button
              variant="ghost"
              size="sm"
              className="mt-3"
              onClick={() => { setJobId(null); setFiles([]); }}
            >
              Start new batch
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
