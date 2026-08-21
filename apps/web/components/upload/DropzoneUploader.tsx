"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";
import { clsx } from "clsx";
import { Spinner } from "@/components/ui/Spinner";

interface DropzoneUploaderProps {
  onFile: (file: File) => void;
  isLoading?: boolean;
}

const ACCEPTED = {
  "image/jpeg": [".jpg", ".jpeg"],
  "image/png": [".png"],
  "image/webp": [".webp"],
};

export function DropzoneUploader({ onFile, isLoading }: DropzoneUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [dragError, setDragError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[], rejections: any[]) => {
      setDragError(null);
      if (rejections.length > 0) {
        setDragError("Please upload a JPEG, PNG, or WebP image (max 10 MB).");
        return;
      }
      const file = acceptedFiles[0];
      if (!file) return;

      const url = URL.createObjectURL(file);
      setPreview(url);
      onFile(file);
    },
    [onFile]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED,
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled: isLoading,
  });

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        id="dropzone-single"
        {...getRootProps()}
        className={clsx(
          "relative rounded-2xl border-2 border-dashed transition-all duration-300 cursor-pointer group",
          isDragActive
            ? "border-brand-400 bg-brand-500/10 glow-border"
            : "border-white/10 hover:border-brand-500/50 hover:bg-white/[0.02]",
          isLoading && "pointer-events-none opacity-60"
        )}
      >
        <input {...getInputProps()} id="dropzone-input" />

        {preview ? (
          <div className="relative aspect-video overflow-hidden rounded-xl">
            <Image
              src={preview}
              alt="Preview"
              fill
              className="object-contain"
              unoptimized
            />
            {isLoading && (
              <div className="absolute inset-0 flex items-center justify-center bg-void-950/70 rounded-xl">
                <Spinner size="lg" />
              </div>
            )}
            {/* Overlay hint */}
            <div className="absolute inset-0 flex items-center justify-center bg-void-950/0 hover:bg-void-950/60 transition-all duration-200 rounded-xl">
              <p className="text-white/0 group-hover:text-white/80 transition-all duration-200 text-sm font-medium">
                Drop a new image to replace
              </p>
            </div>
          </div>
        ) : (
          <div className="py-16 px-8 flex flex-col items-center text-center">
            <div
              className={clsx(
                "w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transition-all duration-300",
                isDragActive
                  ? "bg-brand-500/30 text-brand-300 scale-110"
                  : "bg-white/5 text-slate-500 group-hover:bg-brand-500/10 group-hover:text-brand-400"
              )}
            >
              <svg viewBox="0 0 24 24" className="w-8 h-8" fill="none" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
              </svg>
            </div>
            <p className="text-white font-medium mb-1">
              {isDragActive ? "Drop it here!" : "Drag & drop your image"}
            </p>
            <p className="text-slate-500 text-sm mb-4">or click to browse</p>
            <p className="text-slate-600 text-xs">JPEG, PNG, WebP — max 10 MB</p>
          </div>
        )}
      </div>

      {dragError && (
        <p className="text-red-400 text-sm text-center">{dragError}</p>
      )}
    </div>
  );
}
