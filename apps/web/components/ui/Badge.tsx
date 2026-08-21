import { clsx } from "clsx";

type BadgeVariant = "default" | "success" | "warning" | "danger" | "info" | "purple";

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

const variants: Record<BadgeVariant, string> = {
  default: "bg-white/10 text-slate-300",
  success: "bg-accent-green/15 text-accent-green border border-accent-green/25",
  warning: "bg-accent-amber/15 text-accent-amber border border-accent-amber/25",
  danger: "bg-red-500/15 text-red-400 border border-red-500/25",
  info: "bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/25",
  purple: "bg-brand-500/15 text-brand-300 border border-brand-500/25",
};

export function Badge({ children, variant = "default", className }: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold",
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
