'use client';
import React from 'react';
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const darkLayout = {
  paper_bgcolor: '#0E131F',
  plot_bgcolor: '#0E131F',
  font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 12 },
  margin: { t: 20, r: 20, b: 40, l: 60 },
  gridcolor: 'rgba(255,255,255,0.06)',
  zerolinecolor: 'rgba(255,255,255,0.08)',
};

export default function LanguagePie({ langDist }: { langDist?: Record<string, number> }) {
  if (!langDist || Object.keys(langDist).length === 0) {
    return <div className="text-slate-500 text-sm flex items-center justify-center h-full">No language distribution data</div>;
  }
  const labels = Object.keys(langDist);
  const values = Object.values(langDist);

  const colors = labels.map(label => {
    switch (label) {
      case 'Python': return '#3B82F6';
      case 'JavaScript': return '#F59E0B';
      case 'TypeScript': return '#06B6D4';
      case 'HTML': return '#EF4444';
      case 'CSS': return '#8B5CF6';
      default: return '#94A3B8';
    }
  });

  return (
    <Plot
      data={[{
        type: 'pie',
        labels,
        values,
        hole: 0.65,
        marker: { colors },
        textinfo: 'label+percent',
        hoverinfo: 'label+value',
      }]}
      layout={{
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 11 },
        showlegend: true,
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: -0.1 },
        height: 280,
        margin: { t: 10, b: 30, l: 10, r: 10 },
      }}
      useResizeHandler
      style={{ width: '100%', height: '100%' }}
    />
  );
}
