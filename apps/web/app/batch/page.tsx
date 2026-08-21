"use client";

import { useState } from "react";
import { Navbar } from "@/components/ui/Navbar";
import { BatchUploadGrid } from "@/components/upload/BatchUploadGrid";
import type { Metadata } from "next";

export default function BatchPage() {
  return (
    <div className="min-h-screen bg-void-950">
      <Navbar />
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 right-1/4 w-[600px] h-[400px] bg-accent-cyan/5 rounded-full blur-[100px]" />
        <div className="absolute top-1/2 left-1/4 w-[400px] h-[400px] bg-brand-500/8 rounded-full blur-[80px]" />
      </div>

      <main className="relative max-w-6xl mx-auto px-4 pt-28 pb-20">
        <div className="mb-10 animate-fade-in">
          <h1 className="text-4xl font-bold text-white mb-2">
            Batch <span className="text-gradient">Upload</span>
          </h1>
          <p className="text-slate-400">
            Upload up to 20 images at once. Jobs are processed asynchronously via the background queue.
          </p>
        </div>

        <BatchUploadGrid />
      </main>
    </div>
  );
}
