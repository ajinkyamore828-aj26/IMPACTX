import React from 'react';
import Link from 'next/link';

export default function Sidebar() {
  return (
    <div className="sidebar flex flex-col h-full">
      <div className="mb-6 flex items-center space-x-3">
        <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="14" fill="#1E1B4B" stroke="#6366F1" strokeWidth="2"/>
          <circle cx="16" cy="16" r="6" fill="#818CF8"/>
        </svg>
        <div>
          <div className="font-bold text-white leading-tight">impactx</div>
          <div className="text-[10px] text-indigo-400 font-semibold tracking-wide uppercase">ML Platform</div>
        </div>
      </div>
      <Link href="/upload" className="btn-secondary text-xs py-2 w-full text-center mb-6 block">Start Over</Link>
      <div className="h-px bg-white/10 mb-6"></div>
      
      <div className="bg-[#0E131F] rounded-lg p-4 border border-white/10 mb-auto">
        <div className="text-xs font-bold text-slate-400 uppercase mb-3 tracking-wider">Engine Status</div>
        <div className="space-y-3">
          <div className="flex items-center text-sm">
            <span className="status-dot"></span>
            <span className="text-slate-200 text-xs">Engine Online</span>
          </div>
          <div className="flex items-center text-sm">
            <span className="status-dot"></span>
            <span className="text-slate-200 text-xs">Models: XGBoost & RF</span>
          </div>
          <div className="flex items-center text-sm">
            <span className="status-dot"></span>
            <span className="text-slate-200 text-xs">Groq AI Connected</span>
          </div>
        </div>
      </div>
      <div className="mt-6 text-center text-[10px] text-slate-500">impactx v2.1</div>
    </div>
  );
}
