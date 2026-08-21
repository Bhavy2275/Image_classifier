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
        // Dark glassmorphism palette
        void: {
          950: "#03020a",
          900: "#06050f",
          800: "#0c0b1a",
          700: "#131124",
        },
        brand: {
          50:  "#f0e6ff",
          100: "#dcc8ff",
          200: "#c29eff",
          300: "#a574ff",
          400: "#8b4aff",
          500: "#7c3aed",  // primary purple
          600: "#6d28d9",
          700: "#5b21b6",
          800: "#4c1d95",
          900: "#3b1573",
        },
        accent: {
          cyan:  "#22d3ee",
          pink:  "#f472b6",
          green: "#34d399",
          amber: "#fbbf24",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
      backgroundImage: {
        "radial-brand": "radial-gradient(ellipse at top, #7c3aed22 0%, transparent 60%)",
        "mesh-gradient":
          "linear-gradient(135deg, #06050f 0%, #0c0b1a 50%, #06050f 100%)",
      },
      animation: {
        "glow-pulse": "glow-pulse 3s ease-in-out infinite",
        "fade-in": "fade-in 0.4s ease-out",
        "slide-up": "slide-up 0.5s ease-out",
        "shimmer": "shimmer 1.5s infinite",
      },
      keyframes: {
        "glow-pulse": {
          "0%, 100%": { boxShadow: "0 0 20px 4px rgba(124, 58, 237, 0.2)" },
          "50%": { boxShadow: "0 0 40px 8px rgba(124, 58, 237, 0.4)" },
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
