'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import {
  Code2,
  Network,
  Cpu,
  FileText,
  ArrowRight,
} from 'lucide-react';

export default function StepsPage() {
  const router = useRouter();

  const handleProceed = () => {
    localStorage.setItem('prevView', 'steps');
    router.push('/upload');
  };

  return (
    <div className="min-h-screen bg-bg-page text-white flex flex-col">
      <Navbar currentView="steps" />

      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-10">
        {/* Header */}
        <div className="text-center mb-10">
          <span className="text-[10px] font-mono tracking-widest text-slate-400 bg-white/5 border border-white/10 px-3 py-1 rounded-full uppercase inline-block mb-3">
            EXECUTION WORKFLOW
          </span>
          <h1 className="text-3xl font-extrabold text-white tracking-tight mb-3">
            4-Stage Analysis Pipeline
          </h1>
          <p className="text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
            How impactx transforms raw repository archives into predictive graph intelligence and actionable risk audits.
          </p>
        </div>

        {/* 2x2 Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 max-w-5xl mx-auto mb-10">
          {/* Card 01 */}
          <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-6 flex flex-col justify-between shadow-sm">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center">
                  <span className="text-xs font-mono font-bold text-slate-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md mr-3">
                    01
                  </span>
                  <h3 className="text-white font-bold text-sm md:text-base">Code Ingestion &amp; AST Parsing</h3>
                </div>
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400">
                  <Code2 className="w-4 h-4" />
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-5">
                Uploaded ZIP archives are safely unpacked in an isolated local sandbox. Multi-language AST parsers extract imports, exports, functions, and classes across Python, JS, TS, HTML, and CSS.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                Zip-Slip Traversal Guard
              </span>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                AST Tokenizer
              </span>
            </div>
          </div>

          {/* Card 02 */}
          <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-6 flex flex-col justify-between shadow-sm">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center">
                  <span className="text-xs font-mono font-bold text-slate-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md mr-3">
                    02
                  </span>
                  <h3 className="text-white font-bold text-sm md:text-base">Topology Compilation &amp; Metrics</h3>
                </div>
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400">
                  <Network className="w-4 h-4" />
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-5">
                A directed NetworkX graph is generated to map every dependency relationship. Computes PageRank centrality, in/out degrees, architectural hubs, and detects circular dependency cycles.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                NetworkX DiGraph
              </span>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                Tarjan Cycles
              </span>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                PageRank
              </span>
            </div>
          </div>

          {/* Card 03 */}
          <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-6 flex flex-col justify-between shadow-sm">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center">
                  <span className="text-xs font-mono font-bold text-slate-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md mr-3">
                    03
                  </span>
                  <h3 className="text-white font-bold text-sm md:text-base">Machine Learning Inference</h3>
                </div>
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400">
                  <Cpu className="w-4 h-4" />
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-5">
                Engineered topological features feed into ML models: XGBoost predicts downstream blast radius probability, while Random Forest scores non-use confidence for dead code detection.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                XGBoost Classifier
              </span>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                Random Forest
              </span>
            </div>
          </div>

          {/* Card 04 */}
          <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-6 flex flex-col justify-between shadow-sm">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center">
                  <span className="text-xs font-mono font-bold text-slate-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md mr-3">
                    04
                  </span>
                  <h3 className="text-white font-bold text-sm md:text-base">Interactive Dashboard &amp; Audit Reports</h3>
                </div>
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400">
                  <FileText className="w-4 h-4" />
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-5">
                Interactively simulate change scenarios, inspect architectural hubs, filter dead code, and generate compliance-ready audit reports exportable to PDF, DOCX, and CSV.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                PDF Audit Reports
              </span>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                Word DOCX
              </span>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                CSV Export
              </span>
            </div>
          </div>
        </div>

        {/* Proceed CTA Button */}
        <div className="max-w-md mx-auto mb-10">
          <button
            onClick={handleProceed}
            className="w-full bg-[#4F46E5] hover:bg-[#4338CA] text-white text-sm font-semibold py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2 shadow-sm cursor-pointer"
          >
            <span>Proceed to Codebase Upload</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Footer */}
        <div className="border-t border-white/[0.08] pt-8 pb-4 text-center">
          <div className="font-semibold text-xs text-slate-300 mb-1">
            impactx &mdash; Enterprise Code Change Impact &amp; Architecture ML Platform
          </div>
          <div className="text-[11px] text-slate-500">
            Local Offline Execution &bull; Multi-Language AST &bull; ML Blast Radius &amp; Dead Code Inference
          </div>
        </div>
      </main>
    </div>
  );
}
