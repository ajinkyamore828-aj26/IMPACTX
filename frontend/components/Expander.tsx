import React, { useState } from 'react';

interface ExpanderProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

export default function Expander({ title, children, defaultOpen = false }: ExpanderProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="glass-card mb-6 overflow-hidden">
      <div 
        className="px-5 py-3.5 flex items-center gap-2.5 cursor-pointer select-none hover:bg-white/[0.02] transition-colors"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className={`text-slate-400 text-xs transition-transform duration-200 ${isOpen ? 'rotate-90' : ''}`}>
          ▶
        </span>
        <span className="text-sm font-bold text-white tracking-wide">{title}</span>
      </div>
      {isOpen && (
        <div className="px-6 py-5 border-t border-white/5 bg-[#080D1A]/40">
          {children}
        </div>
      )}
    </div>
  );
}
