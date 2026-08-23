"use client";

import { useState } from "react";
import Image from "next/image";
import type { PredictionResult } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ConfidenceChart } from "./ConfidenceChart";
import { HeatmapOverlay } from "./HeatmapOverlay";

interface PredictionCardProps {
  result: PredictionResult;
}

export function PredictionCard({ result }: PredictionCardProps) {
  const [showHeatmap, setShowHeatmap] = useState(false);
  const top = result.top_classes[0];
  const pct = Math.round(top.confidence * 100);

  return (
    <div className="glass-strong rounded-3xl overflow-hidden glow-border">
      {/* Image with optional heatmap */}
      <div className="relative aspect-video bg-void-800">
        <Image
          src={result.image_url}
          alt={top.label}
          fill
          className="object-contain"
          unoptimized
          priority
        />
        {result.heatmap_base64 && (
          <HeatmapOverlay
            heatmapBase64={result.heatmap_base64}
            visible={showHeatmap}
          />
        )}
      </div>

      <div className="p-6 space-y-5">
        {/* Top prediction */}
        <div className="flex items-start justify-between gap-3">
          <div>
            <span className="text-xs font-mono font-bold text-green-400">DONE</span>
            <p className="text-slate-400 text-xs uppercase tracking-widest mb-1">
              Top prediction
            </p>
            <h2 className="text-white font-bold text-xl capitalize">{top.label}</h2>
          </div>
          <div className="w-10 h-10 mb-3 mx-auto border border-white/10 rounded-xl flex items-center justify-center">
            <span className="text-[10px] font-mono text-white/30">IMG</span>
          </div>
          <div className="text-right">
            <Badge variant={pct >= 80 ? "success" : pct >= 50 ? "warning" : "default"}>
              {pct}% confidence
            </Badge>
            {result.processing_time_ms && (
              <p className="text-slate-500 text-xs mt-1">
                {result.processing_time_ms.toFixed(0)}ms
              </p>
            )}
          </div>
        </div>

        {/* Heatmap toggle */}
        {result.heatmap_base64 && (
          <div className="flex items-center gap-3">
            <Button
              id="heatmap-toggle"
              variant={showHeatmap ? "primary" : "secondary"}
              size="sm"
              onClick={() => setShowHeatmap((v) => !v)}
            >
              {showHeatmap ? "Hide Grad-CAM" : "Show Grad-CAM"}
            </Button>
            {showHeatmap && (
              <p className="text-slate-400 text-xs">
                Highlighted regions drove the prediction
              </p>
            )}
          </div>
        )}

        {/* Confidence chart */}
        <div>
          <p className="text-slate-400 text-xs uppercase tracking-widest mb-3">
            Top 5 classes
          </p>
          <ConfidenceChart classes={result.top_classes} />
        </div>

        {/* Metadata */}
        {result.prediction_id && (
          <p className="text-slate-600 text-xs font-mono">
            ID: {result.prediction_id}
          </p>
        )}
      </div>
    </div>
  );
}
