import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./hooks/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Monochrome palette
        void: {
          950: "#000000",
          900: "#080808",
          800: "#111111",
          700: "#1a1a1a",
        },
        brand: {
          50:  "#ffffff",
          100: "#f5f5f5",
          200: "#e5e5e5",
          300: "#d4d4d4",
          400: "#a3a3a3",
          500: "#ffffff",  // primary: white
          600: "#e5e5e5",
          700: "#a3a3a3",
          800: "#525252",
          900: "#262626",
        },
        accent: {
          cyan:  "#e5e5e5",
          pink:  "#d4d4d4",
          green: "#a3a3a3",
          amber: "#f5f5f5",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
      backgroundImage: {
        "radial-brand": "radial-gradient(ellipse at top, rgba(255,255,255,0.04) 0%, transparent 60%)",
        "mesh-gradient":
          "linear-gradient(135deg, #000000 0%, #111111 50%, #000000 100%)",
      },
      animation: {
        "glow-pulse": "glow-pulse 3s ease-in-out infinite",
        "fade-in": "fade-in 0.4s ease-out",
        "slide-up": "slide-up 0.5s ease-out",
        "shimmer": "shimmer 1.5s infinite",
      },
      keyframes: {
        "glow-pulse": {
          "0%, 100%": { boxShadow: "0 0 20px 4px rgba(255, 255, 255, 0.06)" },
          "50%": { boxShadow: "0 0 40px 8px rgba(255, 255, 255, 0.12)" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(24px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};

export default config;
