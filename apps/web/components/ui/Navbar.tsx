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
        <span className="font-bold text-white text-lg tracking-tight group-hover:text-white/70 transition-colors duration-200">
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
                ? "bg-white/10 text-white"
                : "text-white/40 hover:text-white hover:bg-white/5"
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
        className="px-4 py-2 bg-white hover:bg-white/90 text-black text-sm font-semibold rounded-xl transition-all duration-200 hover:shadow-[0_0_16px_rgba(255,255,255,0.15)]"
      >
        Get Started
      </Link>
    </nav>
  );
}
