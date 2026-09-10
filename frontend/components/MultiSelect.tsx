'use client';

import React, { useState, useRef, useEffect } from 'react';

interface MultiSelectProps {
  label: string;
  hasHelp?: boolean;
  helpText?: string;
  options: { id: string; label: string }[];
  selected: string[];
  onChange: (selected: string[]) => void;
}

export default function MultiSelect({
  label,
  hasHelp = false,
  helpText = '',
  options,
  selected,
  onChange,
}: MultiSelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleRemove = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    onChange(selected.filter(item => item !== id));
  };

  const handleClearAll = (e: React.MouseEvent) => {
    e.stopPropagation();
    onChange([]);
  };

  const handleToggle = (id: string) => {
    if (selected.includes(id)) {
      onChange(selected.filter(item => item !== id));
    } else {
      onChange([...selected, id]);
    }
  };

  return (
    <div className="relative w-full select-none" ref={containerRef}>
      {/* Label Row */}
      <div className="flex items-center justify-between mb-1.5">
        <div className="flex items-center gap-1.5">
          <label className="text-xs font-semibold text-slate-200 tracking-wide">{label}</label>
          {hasHelp && (
            <span
              title={helpText || 'Filter options'}
              className="inline-flex items-center justify-center w-3.5 h-3.5 rounded-full border border-slate-500 text-[9px] text-slate-400 cursor-help"
            >
              ?
            </span>
          )}
        </div>
      </div>

      {/* Multiselect Input Box */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        className={`min-h-[40px] w-full bg-[#080D1A] border rounded-lg px-2.5 py-1.5 flex items-center justify-between cursor-pointer transition-all ${
          isOpen ? 'border-indigo-500 ring-1 ring-indigo-500/20' : 'border-white/10 hover:border-white/20'
        }`}
      >
        <div className="flex flex-wrap items-center gap-1.5 flex-1 pr-2">
          {selected.map(id => {
            const opt = options.find(o => o.id === id);
            const displayLabel = opt ? opt.label : id;
            return (
              <span
                key={id}
                className="bg-[#4F46E5] text-white text-xs font-semibold px-2 py-0.5 rounded flex items-center gap-1.5 shadow-sm"
              >
                <span>{displayLabel}</span>
                <button
                  type="button"
                  onClick={(e) => handleRemove(id, e)}
                  className="text-white/80 hover:text-white text-[11px] leading-none focus:outline-none"
                >
                  ✕
                </button>
              </span>
            );
          })}
          {selected.length === 0 && (
            <span className="text-slate-500 text-xs">Select options...</span>
          )}
        </div>

        {/* Action icons on right */}
        <div className="flex items-center gap-2 text-slate-400 pl-1 flex-shrink-0">
          {selected.length > 0 && (
            <button
              type="button"
              onClick={handleClearAll}
              title="Clear all"
              className="hover:text-white text-xs leading-none focus:outline-none"
            >
              ⊗
            </button>
          )}
          <span className={`text-[9px] text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}>
            ▼
          </span>
        </div>
      </div>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute left-0 right-0 top-full mt-1 bg-[#0D1220] border border-white/15 rounded-lg shadow-2xl z-50 max-h-56 overflow-y-auto py-1 divide-y divide-white/5">
          {options.map(opt => {
            const isSel = selected.includes(opt.id);
            return (
              <div
                key={opt.id}
                onClick={() => handleToggle(opt.id)}
                className={`px-3 py-2 text-xs flex items-center justify-between cursor-pointer hover:bg-white/5 transition-colors ${
                  isSel ? 'text-indigo-400 font-semibold' : 'text-slate-300'
                }`}
              >
                <span>{opt.label}</span>
                {isSel && <span className="text-indigo-400 font-bold">✓</span>}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
