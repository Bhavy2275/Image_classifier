"use client";

import { useEffect, useRef } from "react";

interface HeatmapOverlayProps {
  /** Base64-encoded PNG returned from the /predict endpoint */
  heatmapBase64: string;
  /** Whether to show the overlay */
  visible: boolean;
  /** CSS opacity for the heatmap overlay (default 0.6) */
  opacity?: number;
}

/**
 * Renders the Grad-CAM heatmap as a semi-transparent canvas layer
 * positioned absolutely to fill its parent container.
 *
 * Parent must have `position: relative` and known dimensions.
 */
export function HeatmapOverlay({
  heatmapBase64,
  visible,
  opacity = 0.6,
}: HeatmapOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new window.Image();
    img.onload = () => {
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.globalAlpha = 1;
      ctx.drawImage(img, 0, 0);
    };
    img.src = `data:image/png;base64,${heatmapBase64}`;
  }, [heatmapBase64]);

  return (
    <canvas
      ref={canvasRef}
      id="heatmap-canvas"
      className="absolute inset-0 w-full h-full object-contain transition-opacity duration-400 pointer-events-none"
      style={{ opacity: visible ? opacity : 0 }}
      aria-hidden="true"
    />
  );
}
