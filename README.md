# VisionAI

**Full-stack image classification SaaS** with explainable AI (Grad-CAM heatmaps), single + batch upload, real-time confidence scoring, and prediction history.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML / Inference | PyTorch, EfficientNet-B0 (timm), ONNX Runtime |
| Explainability | Grad-CAM (`pytorch-grad-cam`) |
| Backend | FastAPI, Pydantic v2, Uvicorn |
| Job Queue | Redis + RQ |
| Database / Auth | Supabase (Postgres + JWT Auth) |
| Image Storage | Cloudinary |
| Frontend | Next.js 15 (App Router), React 19, TypeScript |
| Styling | Tailwind CSS |
| Charts | Recharts |
| State / Data | TanStack Query, Zustand |
| Monorepo | Turborepo + npm workspaces |

---

## Quick Start

### Prerequisites
- Node.js ≥ 20, npm ≥ 10
- Python 3.11+
- Docker + Docker Compose
- [Supabase account](https://supabase.com)
- [Cloudinary account](https://cloudinary.com)

### 1. Clone and configure

```bash
git clone https://github.com/your-org/visionai.git
cd visionai

# Copy and fill in your credentials
cp .env.example .env
```

Edit `.env` with your Supabase, Cloudinary, and Redis credentials.

### 2. Start the full backend stack (API + Redis + Worker)

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.  
The first startup automatically exports the EfficientNet-B0 ONNX model (≈ 30 seconds).

### 3. Start the Next.js frontend

```bash
cd apps/web
npm install
npm run dev
```

Open `http://localhost:3000`.

---

## Supabase Setup

Run the following SQL in your Supabase SQL editor to create the required tables:

```sql
-- Predictions table
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  cloudinary_public_id TEXT,
  top_classes JSONB NOT NULL,
  heatmap_url TEXT,
  batch_job_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own predictions" ON predictions
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own predictions" ON predictions
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Batch jobs table
CREATE TABLE batch_jobs (
  id TEXT PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  status TEXT NOT NULL DEFAULT 'pending',
  total_images INT NOT NULL DEFAULT 0,
  completed_images INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE batch_jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own batch jobs" ON batch_jobs
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own batch jobs" ON batch_jobs
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

---

## Project Structure

```
visionai/
├── apps/
│   ├── web/          # Next.js 15 frontend
│   └── api/          # FastAPI backend + ML inference
├── packages/
│   └── shared-types/ # Shared TypeScript types
├── .github/workflows/ci.yml
├── docker-compose.yml
├── turbo.json
└── .env.example
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Single image inference + Grad-CAM |
| `POST` | `/batch/predict` | Submit batch job (returns job_id) |
| `GET` | `/batch/status/{job_id}` | Poll batch job status |
| `GET` | `/history` | Paginated prediction history |

---

## Deployment

| Service | Platform |
|---------|----------|
| Frontend (`apps/web`) | Vercel |
| Backend + Worker (`apps/api`) | Railway (two services) |
| Database + Auth | Supabase |
| Image Storage | Cloudinary |
| Redis | Railway Redis plugin |

See `.env.example` for all required environment variables.

---

## Development

```bash
# Run all workspace tasks via Turborepo
npm run dev      # Start all dev servers
npm run build    # Build all packages
npm run lint     # Lint all packages
npm test         # Run all tests
```

```bash
# Backend only (without Docker)
cd apps/api
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
# RQ worker (separate terminal)
cd apps/api
rq worker --url redis://localhost:6379/0 visionai-batch
```
