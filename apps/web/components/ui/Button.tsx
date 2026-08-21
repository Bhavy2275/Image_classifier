import { clsx } from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export function Button({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  disabled,
  className,
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 active:scale-95";

  const variants = {
    primary:
      "bg-brand-500 hover:bg-brand-400 text-white shadow-lg hover:shadow-[0_0_24px_rgba(124,58,237,0.4)] disabled:opacity-50",
    secondary:
      "glass hover:glass-strong text-slate-200 border border-white/10 hover:border-white/20 disabled:opacity-50",
    ghost:
      "text-slate-400 hover:text-white hover:bg-white/5 disabled:opacity-50",
    danger:
      "bg-red-600 hover:bg-red-500 text-white disabled:opacity-50",
  };

  const sizes = {
    sm: "text-sm px-3 py-1.5",
    md: "text-sm px-5 py-2.5",
    lg: "text-base px-7 py-3.5",
  };

  return (
    <button
      disabled={disabled || isLoading}
      className={clsx(base, variants[variant], sizes[size], className)}
      {...props}
    >
      {isLoading && (
        <svg
          className="animate-spin h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
      )}
      {children}
    </button>
  );
}
