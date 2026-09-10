import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtext?: string;
}

export default function MetricCard({ title, value, subtext }: MetricCardProps) {
  return (
    <div className="bg-[#0D1220] border border-white/10 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">{title}</div>
        <div className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">{value}</div>
      </div>
      {subtext && <div className="text-[11px] text-slate-500 mt-2 font-medium">{subtext}</div>}
    </div>
  );
}
