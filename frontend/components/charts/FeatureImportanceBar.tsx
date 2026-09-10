'use client';
import React from 'react';
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const darkLayout = {
  paper_bgcolor: '#0E131F',
  plot_bgcolor: '#0E131F',
  font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 12 },
  margin: { t: 40, r: 20, b: 40, l: 120 },
  gridcolor: 'rgba(255,255,255,0.06)',
  zerolinecolor: 'rgba(255,255,255,0.08)',
};

export default function FeatureImportanceBar({ importances, title = "Feature Importance" }: { importances?: Record<string, number>, title?: string }) {
  if (!importances || Object.keys(importances).length === 0) {
    return <div className="text-slate-500 text-sm flex items-center justify-center h-[350px]">No feature importance data</div>;
  }
  const sorted = Object.entries(importances).sort((a, b) => a[1] - b[1]);
  const formatLabel = (s: string) => s.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  const y = sorted.map(i => formatLabel(i[0]));
  const x = sorted.map(i => i[1]);
  const barColors = x.map((val, idx) => idx === x.length - 1 ? '#6D28D9' : '#C7D2FE');

  return (
    <Plot
      data={[{
        type: 'bar',
        x,
        y,
        orientation: 'h',
        marker: { color: barColors }
      }]}
      layout={{
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 11 },
        title: title ? { text: title, font: { color: '#FFFFFF', size: 14 } } : undefined,
        xaxis: { title: { text: 'Importance Weight' }, gridcolor: 'rgba(255,255,255,0.06)', color: '#94A3B8' },
        yaxis: { automargin: true, color: '#94A3B8' },
        height: 330,
        margin: { t: 10, r: 20, b: 40, l: 140 },
      }}
      useResizeHandler
      style={{ width: '100%', height: '100%' }}
    />
  );
}
