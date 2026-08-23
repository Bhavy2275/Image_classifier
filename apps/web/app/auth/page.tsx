"use client";

import { useState, useEffect } from "react";
import { supabase } from "@/lib/supabase-client";
import { useRouter } from "next/navigation";
import { Spinner } from "@/components/ui/Spinner";
import type { Metadata } from "next";

export default function AuthPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (data.session) router.replace("/dashboard");
    });
  }, [router]);

  const handleMagicLink = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/dashboard` },
    });
    setLoading(false);
    if (error) {
      setError(error.message);
    } else {
      setSent(true);
    }
  };

  const handleGitHub = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "github",
      options: { redirectTo: `${window.location.origin}/dashboard` },
    });
  };

  return (
    <div className="min-h-screen bg-void-950 flex items-center justify-center px-4">
      {/* Background glow */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-brand-500/10 rounded-full blur-[100px]" />
      </div>

      <div className="w-full max-w-md relative animate-slide-up">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 bg-brand-500 rounded-xl flex items-center justify-center text-xl">
              ●●●
            </div>
            <span className="text-2xl font-bold text-white">VisionAI</span>
          </div>
          <p className="text-slate-400">Sign in to save your predictions</p>
        </div>

        <div className="glass-strong rounded-3xl p-8">
          {sent ? (
            <div className="text-center py-4">
              <div className="w-12 h-12 mb-4 mx-auto border border-white/10 rounded-xl flex items-center justify-center"><span className="text-xs font-mono text-white/20">AUTH</span></div>
              <h2 className="text-white font-semibold text-xl mb-2">Check your email</h2>
              <p className="text-slate-400 text-sm">
                We sent a magic link to <strong className="text-white">{email}</strong>.
                Click it to sign in instantly.
              </p>
            </div>
          ) : (
            <>
              {/* GitHub OAuth */}
              <button
                id="auth-github"
                onClick={handleGitHub}
                className="w-full flex items-center justify-center gap-3 px-6 py-3 glass hover:glass-strong border border-white/10 hover:border-white/20 text-white font-medium rounded-2xl transition-all duration-200 mb-6"
              >
                <svg viewBox="0 0 24 24" className="w-5 h-5 fill-current">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
                </svg>
                Continue with GitHub
              </button>

              <div className="flex items-center gap-4 mb-6">
                <div className="flex-1 h-px bg-white/10" />
                <span className="text-slate-500 text-sm">or</span>
                <div className="flex-1 h-px bg-white/10" />
              </div>

              {/* Magic link form */}
              <form onSubmit={handleMagicLink} className="space-y-4">
                <div>
                  <label
                    htmlFor="auth-email"
                    className="block text-sm font-medium text-slate-300 mb-2"
                  >
                    Email address
                  </label>
                  <input
                    id="auth-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    required
                    className="w-full px-4 py-3 bg-void-800 border border-white/10 focus:border-brand-500 rounded-xl text-white placeholder-slate-500 outline-none transition-colors"
                  />
                </div>

                {error && (
                  <p className="text-red-400 text-sm bg-red-400/10 px-4 py-2 rounded-xl">
                    {error}
                  </p>
                )}

                <button
                  id="auth-submit"
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 bg-brand-500 hover:bg-brand-400 disabled:opacity-60 text-white font-semibold rounded-xl transition-all duration-200 hover:shadow-[0_0_20px_rgba(124,58,237,0.4)] flex items-center justify-center gap-2"
                >
                  {loading ? <Spinner size="sm" /> : null}
                  Send magic link
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
