import Link from "next/link";
import type { Metadata } from "next";
import { Navbar } from "@/components/ui/Navbar";
import {
  Brain,
  Eye,
  Layers,
  BarChart2,
  Zap,
  Server,
  Image as ImageIcon,
  Scan,
  Car,
  Leaf,
  Feather,
  Music,
  type LucideIcon,
} from "lucide-react";

export const metadata: Metadata = {
  title: "VisionAI — Explainable Image Classification",
};

const features: { Icon: LucideIcon; title: string; description: string }[] = [
  {
    Icon: Brain,
    title: "EfficientNet Backbone",
    description:
      "Powered by EfficientNet-B0 exported to ONNX Runtime for blazing-fast CPU/GPU inference across 1,000 ImageNet classes.",
  },
  {
    Icon: Eye,
    title: "Grad-CAM Explainability",
    description:
      "See exactly what the model 'sees'. Gradient-weighted class activation maps highlight the regions that drove each prediction.",
  },
  {
    Icon: Layers,
    title: "Batch Processing",
    description:
      "Upload up to 20 images at once. Jobs are queued via Redis/RQ so your request never blocks — just poll for results.",
  },
  {
    Icon: BarChart2,
    title: "Confidence Charts",
    description:
      "Interactive Recharts visualizations show the top-5 predicted classes with confidence scores side-by-side.",
  },
  {
    Icon: Zap,
    title: "Real-Time Analysis",
    description:
      "Instant feedback with interactive probability breakdowns and on-the-fly heatmap generation for any uploaded image.",
  },
  {
    Icon: Server,
    title: "Production Ready",
    description:
      "FastAPI + Gunicorn backend. Docker Compose for local dev. Deploys to Railway + Vercel in minutes.",
  },
];

const demoCategories: { Icon: LucideIcon; label: string }[] = [
  { Icon: Scan,    label: "Animal" },
  { Icon: Car,     label: "Vehicle" },
  { Icon: Leaf,    label: "Plant" },
  { Icon: Feather, label: "Bird" },
  { Icon: Music,   label: "Object" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-void-950 overflow-hidden">
      <Navbar />

      {/* ── Background effects ───────────────────────────── */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[600px] bg-white/[0.03] rounded-full blur-[120px]" />
        <div className="absolute top-1/3 left-1/4 w-[400px] h-[400px] bg-white/[0.02] rounded-full blur-[80px]" />
        <div className="absolute bottom-1/4 right-1/4 w-[300px] h-[300px] bg-white/[0.02] rounded-full blur-[80px]" />
      </div>

      {/* ── Hero ─────────────────────────────────────────── */}
      <section className="relative pt-36 pb-24 px-4 text-center animate-fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-white/15 text-white/60 text-sm font-medium mb-8">
          <span className="w-2 h-2 bg-white/70 rounded-full animate-pulse" />
          Powered by EfficientNet + ONNX Runtime
        </div>

        <h1 className="text-5xl sm:text-7xl font-black tracking-tight mb-6 max-w-4xl mx-auto leading-none">
          <span className="text-white">See what your</span>
          <br />
          <span className="text-gradient">AI actually sees</span>
        </h1>

        <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed">
          Upload any image and get instant classification across 1,000 categories —
          with Grad-CAM heatmaps that show{" "}
          <em className="text-slate-200 not-italic">exactly</em> which pixels drove the prediction.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/dashboard"
            id="cta-try-demo"
            className="px-8 py-4 bg-white hover:bg-white/90 text-black font-semibold rounded-2xl transition-all duration-200 hover:shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:scale-105 active:scale-100 text-lg"
          >
            Try it free →
          </Link>
          <Link
            href="/batch"
            id="cta-batch"
            className="px-8 py-4 glass border border-white/15 hover:glass-strong text-white/80 font-semibold rounded-2xl transition-all duration-200 hover:scale-105 text-lg"
          >
            Batch upload
          </Link>
        </div>
      </section>

      {/* ── Demo image strip ─────────────────────────────── */}
      <section className="relative px-4 pb-24 max-w-5xl mx-auto animate-slide-up">
        <div className="glass rounded-3xl p-6 glow-border">
          <div className="bg-void-800 rounded-2xl aspect-[16/7] flex items-center justify-center overflow-hidden">
            <div className="text-center text-white/20 flex flex-col items-center">
              <ImageIcon className="w-12 h-12 mb-3 text-white/15" strokeWidth={1} />
              <p className="text-sm">Drag &amp; drop any image to classify</p>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-5 gap-3">
            {demoCategories.map(({ Icon, label }, i) => (
              <div
                key={i}
                className="bg-void-800 rounded-xl aspect-square flex flex-col items-center justify-center gap-1.5 hover:scale-105 transition-transform cursor-pointer group"
              >
                <Icon className="w-5 h-5 text-white/25 group-hover:text-white/50 transition-colors" strokeWidth={1.5} />
                <span className="text-[9px] font-medium text-white/20 group-hover:text-white/40 transition-colors tracking-wide">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ─────────────────────────────────────── */}
      <section className="relative px-4 pb-32 max-w-6xl mx-auto">
        <h2 className="text-3xl sm:text-4xl font-bold text-center mb-4 text-white">
          Everything you need
        </h2>
        <p className="text-slate-400 text-center mb-16 max-w-xl mx-auto">
          Production-grade ML infrastructure with a beautiful developer experience.
        </p>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map(({ Icon, title, description }, i) => (
            <div
              key={i}
              className="glass rounded-2xl p-6 hover:glass-strong transition-all duration-300 hover:scale-[1.02] hover:glow-border group"
            >
              <div className="w-10 h-10 rounded-xl border border-white/10 bg-white/5 flex items-center justify-center mb-4 group-hover:border-white/20 group-hover:bg-white/8 transition-all duration-200">
                <Icon className="w-5 h-5 text-white/50 group-hover:text-white/80 transition-colors" strokeWidth={1.5} />
              </div>
              <h3 className="text-white font-semibold text-lg mb-2">{title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────── */}
      <footer className="border-t border-white/5 py-10 px-4">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-white/30">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-white/50">VisionAI</span>
            <span>—</span>
            <span>Built with FastAPI, Next.js &amp; PyTorch</span>
          </div>
          <div className="flex items-center gap-4">
            <span>© {new Date().getFullYear()} Bhavya</span>
            <a
              href="https://github.com/Bhavy2275/Image_classifier"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white/60 transition-colors underline underline-offset-2"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
