"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { clsx } from "clsx";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/batch", label: "Batch" },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 glass border-b border-white/5">
      {/* Logo */}
      <Link href="/" className="flex items-center group">
        <span className="font-bold text-white text-lg tracking-tight group-hover:text-brand-300 transition-colors duration-200">
          VisionAI
        </span>
      </Link>

      {/* Nav links */}
      <div className="hidden sm:flex items-center gap-1">
        {links.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              "px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200",
              pathname === href
                ? "bg-brand-500/20 text-brand-300"
                : "text-slate-400 hover:text-white hover:bg-white/5"
            )}
          >
            {label}
          </Link>
        ))}
      </div>

      {/* App CTA */}
      <Link
        href="/dashboard"
        id="navbar-cta"
        className="px-4 py-2 bg-brand-500 hover:bg-brand-400 text-white text-sm font-semibold rounded-xl transition-all duration-200 hover:shadow-[0_0_16px_rgba(124,58,237,0.4)]"
      >
        Get Started
      </Link>
    </nav>
  );
}
