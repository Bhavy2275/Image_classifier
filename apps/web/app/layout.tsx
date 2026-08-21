import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "VisionAI — Explainable Image Classification",
    template: "%s | VisionAI",
  },
  description:
    "State-of-the-art image classification with Grad-CAM explainability, batch processing, and real-time confidence scoring.",
  keywords: ["image classification", "AI", "machine learning", "Grad-CAM", "explainable AI"],
  openGraph: {
    title: "VisionAI — Explainable Image Classification",
    description: "Upload any image and get instant AI classification with visual explanations.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
