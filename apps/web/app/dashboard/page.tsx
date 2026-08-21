"use client";

import { useState } from "react";
import type { Metadata } from "next";
import { Navbar } from "@/components/ui/Navbar";
import { DropzoneUploader } from "@/components/upload/DropzoneUploader";
import { PredictionCard } from "@/components/results/PredictionCard";
import { useUploadImage } from "@/hooks/useUploadImage";
import type { PredictionResult } from "@/lib/types";
import { Spinner } from "@/components/ui/Spinner";

export default function DashboardPage() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const { mutate, isPending, error } = useUploadImage({
    onSuccess: (data) => setResult(data),
  });

  const handleFile = (file: File) => {
    setResult(null);
    mutate({ file, includeHeatmap: true });
  };

  return (
    <div className="min-h-screen bg-void-950">
      <Navbar />

      {/* Background glow */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-brand-500/8 rounded-full blur-[100px]" />
      </div>

      <main className="relative max-w-6xl mx-auto px-4 pt-28 pb-20">
        <div className="mb-10 animate-fade-in">
          <h1 className="text-4xl font-bold text-white mb-2">
            Image <span className="text-gradient">Dashboard</span>
          </h1>
          <p className="text-slate-400">
            Upload an image to classify it across 1,000 ImageNet categories with Grad-CAM explainability.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 animate-slide-up">
          {/* ── Upload panel ─────────────────────────── */}
          <div className="space-y-6">
            <div className="glass rounded-3xl p-6">
              <h2 className="text-white font-semibold text-lg mb-4">Upload Image</h2>
              <DropzoneUploader onFile={handleFile} isLoading={isPending} />
            </div>

            {error && (
              <div className="glass rounded-2xl p-4 border border-red-500/30 text-red-400 text-sm">
                ❌ {error.message}
              </div>
            )}

            {isPending && (
              <div className="glass rounded-2xl p-6 flex items-center gap-4">
                <Spinner />
                <div>
                  <p className="text-white font-medium">Classifying image…</p>
                  <p className="text-slate-400 text-sm">Running ONNX inference + Grad-CAM</p>
                </div>
              </div>
            )}
          </div>

          {/* ── Results panel ────────────────────────── */}
          <div>
            {result ? (
              <div className="animate-slide-up">
                <PredictionCard result={result} />
              </div>
            ) : (
              <div className="glass rounded-3xl p-8 h-full flex flex-col items-center justify-center text-center min-h-[320px]">
                <div className="text-5xl mb-4 opacity-30">🎯</div>
                <p className="text-slate-500 text-sm">
                  Your prediction results will appear here after upload.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Quick links */}
        <div className="mt-12 grid sm:grid-cols-2 gap-4 animate-fade-in">
          <a href="/batch" className="glass rounded-2xl p-5 hover:glass-strong transition-all duration-200 hover:glow-border group">
            <div className="flex items-center gap-3">
              <span className="text-2xl group-hover:scale-110 transition-transform">📦</span>
              <div>
                <p className="text-white font-medium">Batch Upload</p>
                <p className="text-slate-400 text-sm">Process up to 20 images at once</p>
              </div>
            </div>
          </a>
          <a href="/dashboard/history" className="glass rounded-2xl p-5 hover:glass-strong transition-all duration-200 hover:glow-border group">
            <div className="flex items-center gap-3">
              <span className="text-2xl group-hover:scale-110 transition-transform">📜</span>
              <div>
                <p className="text-white font-medium">History</p>
                <p className="text-slate-400 text-sm">View your past predictions</p>
              </div>
            </div>
          </a>
        </div>
      </main>
    </div>
  );
}
