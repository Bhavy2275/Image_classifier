# VisionAI — Explainable Image Classification SaaS

[![Live Demo](https://img.shields.io/badge/Live_Demo-VisionAI-7c3aed?style=for-the-badge&logo=vercel)]([https://visiona1.vercel.app](https://visiona1.vercel.app/)) *(Replace with your live deployment URL)*

VisionAI is an AI-powered image classification platform that provides instant predictions across 1,000 categories alongside Grad-CAM heatmaps to explain exactly what visual features influenced the model's decisions.

---

## 🌐 Live Application

- **Live URL:** [https://visionai.vercel.app](https://visionai.vercel.app)

---

## 📖 How to Use the Application

### 1. Single Image Classification & Explainability
1. Go to the **Dashboard** (`/dashboard`).
2. **Upload an Image:** Drag and drop any image (`.jpg`, `.jpeg`, `.png`, `.webp`) or click the upload area to select a file from your device.
3. **Analyze Results:**
   - **Top Predictions:** View the top-5 predicted classes along with interactive confidence score bars.
   - **Grad-CAM Heatmap:** Toggle the heatmap overlay to see which specific regions of the image drove the model's classification.
   - **Export Details:** Review and share prediction scores and heatmap outputs.

---

### 2. Batch Image Processing
1. Navigate to the **Batch Upload** page (`/batch`).
2. **Select Multiple Images:** Drag and drop up to 20 images at once.
3. **Start Batch Job:** Click **Process Batch** to submit the images to the asynchronous processing queue.
4. **Monitor Progress:** Track the real-time progress bar as each image is analyzed.
5. **View Batch Results:** Inspect the individual predictions, confidence scores, and heatmaps for all uploaded images in one consolidated view.
