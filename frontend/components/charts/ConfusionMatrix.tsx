'use client';
import React from 'react';
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const darkLayout = {
  paper_bgcolor: '#0E131F',
  plot_bgcolor: '#0E131F',
  font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 12 },
  margin: { t: 40, r: 20, b: 40, l: 60 },
  gridcolor: 'rgba(255,255,255,0.06)',
  zerolinecolor: 'rgba(255,255,255,0.08)',
};

export default function ConfusionMatrix({ cm }: { cm?: number[][] }) {
  if (!cm || !Array.isArray(cm) || cm.length === 0) {
    return <div className="text-slate-500 text-sm flex items-center justify-center h-[350px]">No confusion matrix data</div>;
  }
  const annotations: any[] = [];
  for (let i = 0; i < cm.length; i++) {
    for (let j = 0; j < (cm[i] || []).length; j++) {
      const val = cm[i][j];
      annotations.push({
        x: ['Predicted Negative', 'Predicted Positive'][j],
        y: ['Actual Negative', 'Actual Positive'][i],
        text: String(val),
        font: { color: val > 200 ? '#FFFFFF' : '#475569', size: 14, family: 'Inter, sans-serif' },
        showarrow: false,
      });
    }
  }

  return (
    <Plot
      data={[{
        z: cm,
        x: ['Predicted Negative', 'Predicted Positive'],
        y: ['Actual Negative', 'Actual Positive'],
        type: 'heatmap',
        colorscale: [
          [0, '#F3E8FF'],
          [0.2, '#DDD6FE'],
          [0.5, '#A855F7'],
          [1, '#4C1D95']
        ],
        showscale: false,
      }]}
      layout={{
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 11 },
        annotations,
        height: 330,
        margin: { t: 20, r: 20, b: 40, l: 110 },
      }}
      useResizeHandler
      style={{ width: '100%', height: '100%' }}
    />
  );
}
