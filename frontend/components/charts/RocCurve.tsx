'use client';
import React from 'react';
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const darkLayout = {
  paper_bgcolor: '#0E131F',
  plot_bgcolor: '#0E131F',
  font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 12 },
  margin: { t: 40, r: 20, b: 40, l: 40 },
  gridcolor: 'rgba(255,255,255,0.06)',
  zerolinecolor: 'rgba(255,255,255,0.08)',
};

export default function RocCurve({ rocData, aucScore }: { rocData?: { fpr: number[], tpr: number[] }, aucScore?: number }) {
  if (!rocData || !rocData.fpr || !rocData.tpr) {
    return <div className="text-slate-500 text-sm flex items-center justify-center h-[350px]">No ROC curve calibration data</div>;
  }
  const safeAuc = typeof aucScore === 'number' ? aucScore : 0;
  return (
    <Plot
      data={[
        {
          x: rocData.fpr,
          y: rocData.tpr,
          type: 'scatter',
          mode: 'lines',
          name: `ROC Curve (AUC = ${safeAuc.toFixed(3)})`,
          line: { color: '#8B5CF6', width: 2 },
        },
        {
          x: [0, 1],
          y: [0, 1],
          type: 'scatter',
          mode: 'lines',
          name: 'Random Baseline',
          line: { color: '#64748B', width: 2, dash: 'dash' },
        },
      ]}
      layout={{
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8', family: 'Inter, sans-serif', size: 11 },
        xaxis: { title: { text: 'False Positive Rate (1 - Specificity)' }, gridcolor: 'rgba(255,255,255,0.06)', color: '#94A3B8' },
        yaxis: { title: { text: 'True Positive Rate (Recall)' }, gridcolor: 'rgba(255,255,255,0.06)', color: '#94A3B8' },
        showlegend: true,
        legend: { x: 0.98, y: 0.98, xanchor: 'right', yanchor: 'top' },
        height: 330,
        margin: { t: 20, r: 20, b: 40, l: 50 },
      }}
      useResizeHandler
      style={{ width: '100%', height: '100%' }}
    />
  );
}
