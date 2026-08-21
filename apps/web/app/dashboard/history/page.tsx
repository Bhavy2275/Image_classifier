"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Navbar } from "@/components/ui/Navbar";
import { getHistory } from "@/lib/api-client";
import type { PredictionHistoryItem } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import Image from "next/image";

export default function HistoryPage() {
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 12;

  const { data, isLoading, error } = useQuery({
    queryKey: ["history", page],
    queryFn: () => getHistory(page, PAGE_SIZE),
  });

  const totalPages = data ? Math.ceil(data.total / PAGE_SIZE) : 0;

  return (
    <div className="min-h-screen bg-void-950">
      <Navbar />
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-brand-500/8 rounded-full blur-[100px]" />
      </div>

      <main className="relative max-w-6xl mx-auto px-4 pt-28 pb-20">
        <div className="mb-10 animate-fade-in">
          <h1 className="text-4xl font-bold text-white mb-2">
            Prediction <span className="text-gradient">History</span>
          </h1>
          <p className="text-slate-400">Your past image classifications.</p>
        </div>

        {isLoading && (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        )}

        {error && (
          <div className="glass rounded-2xl p-6 border border-red-500/30 text-red-400">
            Failed to load history: {(error as Error).message}
          </div>
        )}

        {data && data.items.length === 0 && (
          <div className="glass rounded-3xl p-12 text-center">
            <div className="text-5xl mb-4">📭</div>
            <p className="text-slate-400">No predictions yet. Go classify some images!</p>
          </div>
        )}

        {data && data.items.length > 0 && (
          <>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 animate-slide-up">
              {data.items.map((item: PredictionHistoryItem) => (
                <HistoryCard key={item.id} item={item} />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center gap-2 mt-10">
                <button
                  id="history-prev"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 glass rounded-xl text-slate-300 disabled:opacity-40 hover:glass-strong transition-all"
                >
                  ← Prev
                </button>
                <span className="px-4 py-2 text-slate-400 text-sm flex items-center">
                  {page} / {totalPages}
                </span>
                <button
                  id="history-next"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 glass rounded-xl text-slate-300 disabled:opacity-40 hover:glass-strong transition-all"
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

function HistoryCard({ item }: { item: PredictionHistoryItem }) {
  const top = item.top_classes[0];
  const pct = Math.round(top.confidence * 100);
  const date = new Date(item.created_at).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="glass rounded-2xl overflow-hidden hover:glass-strong hover:glow-border transition-all duration-300 hover:scale-[1.02] group">
      <div className="relative aspect-video bg-void-800">
        <Image
          src={item.image_url}
          alt={top.label}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-500"
          unoptimized
        />
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-2 mb-2">
          <p className="text-white font-semibold text-sm truncate">{top.label}</p>
          <Badge variant="success">{pct}%</Badge>
        </div>
        <p className="text-slate-500 text-xs">{date}</p>
        {item.batch_job_id && (
          <p className="text-slate-600 text-xs mt-1 truncate">
            Batch: {item.batch_job_id.slice(0, 8)}…
          </p>
        )}
      </div>
    </div>
  );
}
