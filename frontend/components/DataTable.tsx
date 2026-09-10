import React from 'react';

interface DataTableProps {
  columns: {key: string; label: string; width?: string}[];
  rows: Record<string, any>[];
  progressColumn?: string;
}

export default function DataTable({ columns, rows, progressColumn }: DataTableProps) {
  return (
    <div className="overflow-x-auto w-full">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-white/10 bg-[#080D1A]/50">
            {columns.map(c => (
              <th key={c.key} style={{ width: c.width }} className="py-3 px-4 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5">
          {rows.map((row, i) => (
            <tr key={i} className="hover:bg-white/[0.02] transition-colors">
              {columns.map(c => (
                <td key={c.key} className="py-2.5 px-4 text-xs text-slate-300 font-normal">
                  {c.key === progressColumn ? (
                    <div className="flex items-center space-x-2.5 min-w-[120px]">
                      <div className="h-1.5 bg-white/10 rounded-full flex-1 overflow-hidden">
                        <div
                          className="h-full bg-indigo-500 rounded-full"
                          style={{ width: `${Math.min(100, Math.max(0, parseFloat(row[c.key] || 0) * 100))}%` }}
                        />
                      </div>
                      <span className="text-[11px] font-mono text-slate-400 w-9 text-right">
                        {(parseFloat(row[c.key] || 0) * 100).toFixed(1)}%
                      </span>
                    </div>
                  ) : (
                    row[c.key]
                  )}
                </td>
              ))}
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="text-center py-6 text-xs text-slate-500">
                No matching data found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
