'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

interface NavbarProps {
  currentView: 'about' | 'steps' | 'projects' | 'dashboard';
  projectName?: string;
}

const Logo = () => (
  <svg width="28" height="28" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ flexShrink: 0 }}>
    <line x1="7" y1="7" x2="25" y2="25" stroke="#818CF8" strokeWidth="2.5" strokeLinecap="round" />
    <line x1="25" y1="7" x2="7" y2="25" stroke="#818CF8" strokeWidth="2.5" strokeLinecap="round" />
    <line x1="7" y1="16" x2="25" y2="16" stroke="#4F46E5" strokeWidth="1.5" strokeDasharray="2 2" strokeLinecap="round" />
    <circle cx="7" cy="7" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
    <circle cx="25" cy="7" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
    <circle cx="7" cy="25" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
    <circle cx="25" cy="25" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
    <circle cx="16" cy="16" r="4.5" fill="#1E1B4B" stroke="#6366F1" strokeWidth="2" />
    <circle cx="16" cy="16" r="2" fill="#818CF8" />
  </svg>
);

export default function Navbar({ currentView, projectName }: NavbarProps) {
  const isNav = currentView === 'about' || currentView === 'steps';
  return (
    <header className="w-full border-b border-white/[0.08] bg-[#080D1A]/95 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 sm:px-8 py-3.5">
        <Link href="/" className="flex items-center space-x-3 hover:opacity-90 transition-opacity">
          <Logo />
          <span className="text-xl font-bold tracking-tight text-white font-mono">impactx</span>
          <span className="bg-white/[0.04] text-slate-300 text-[10px] font-semibold tracking-wider px-2 py-0.5 rounded border border-white/10 uppercase">
            ML PLATFORM
          </span>
          {projectName && (
            <span className="bg-emerald-500/10 text-emerald-400 text-xs font-semibold px-2.5 py-0.5 rounded-md border border-emerald-500/30 ml-2 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              {projectName}
            </span>
          )}
        </Link>

        {isNav && (
          <div className="flex items-center space-x-3">
            <div className="bg-[#0D1220] border border-white/10 p-1 rounded-lg flex items-center space-x-1">
              <Link
                href="/"
                className={`px-5 py-1.5 rounded-md text-xs font-semibold transition-all ${
                  currentView === 'about'
                    ? 'bg-[#4F46E5] text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                About
              </Link>
              <Link
                href="/steps"
                className={`px-5 py-1.5 rounded-md text-xs font-semibold transition-all ${
                  currentView === 'steps'
                    ? 'bg-[#4F46E5] text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Steps
              </Link>
            </div>

            <Link
              href="/upload"
              className="hidden sm:inline-flex items-center gap-1.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white text-xs font-semibold px-3.5 py-1.5 rounded-lg transition-colors shadow-sm"
            >
              <span>Upload Codebase</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
