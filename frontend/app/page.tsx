'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import {
  Zap,
  CircleSlash,
  Code2,
  Network,
  FileText,
  ShieldCheck,
  ArrowRight,
  GitBranch,
  Search,
  Lock,
  Cpu,
  Layers,
  FileCheck2,
  CheckCircle2,
  ChevronRight,
  Database,
  Terminal,
  Activity,
} from 'lucide-react';

interface CapabilityItem {
  icon: React.ReactNode;
  title: string;
  description: string;
  tag: string;
}

const CAPABILITIES: CapabilityItem[] = [
  {
    icon: <Zap className="w-4 h-4 text-indigo-400" />,
    title: 'Change Impact Prediction',
    description: 'Evaluates graph distance hops, coupling degrees, and XGBoost machine learning probabilities to calculate downstream ripple cascade.',
    tag: 'XGBoost Classifier',
  },
  {
    icon: <CircleSlash className="w-4 h-4 text-indigo-400" />,
    title: 'Dead Code Detection',
    description: 'Identifies unreferenced files, classes, and functions using topological PageRank centrality, in-degree coupling, and Random Forest classification.',
    tag: 'Random Forest',
  },
  {
    icon: <Code2 className="w-4 h-4 text-indigo-400" />,
    title: 'Multi-Language AST Engine',
    description: 'Parses code structures across Python AST, JavaScript and TypeScript ES6 / CommonJS modules, HTML DOM, and CSS stylesheets.',
    tag: 'AST Tokenizer',
  },
  {
    icon: <Network className="w-4 h-4 text-indigo-400" />,
    title: 'Dependency Graph Topology',
    description: 'Compiles directed NetworkX graphs to map import chains, compute PageRank centrality, and detect circular dependency cycles.',
    tag: 'NetworkX DiGraph',
  },
  {
    icon: <FileText className="w-4 h-4 text-indigo-400" />,
    title: 'Executive Audit Reports',
    description: 'Generates formal compliance and architecture documentation in PDF, Word (.docx), and CSV formats for pull request reviews.',
    tag: 'PDF & DOCX Export',
  },
  {
    icon: <ShieldCheck className="w-4 h-4 text-indigo-400" />,
    title: '100% Local Sandboxing',
    description: 'Archive extraction, graph compilation, and ML inference execute entirely offline inside your local sandbox with zero data telemetry.',
    tag: 'Zip-Slip Protection',
  },
];

const WORKFLOW_STEPS = [
  {
    step: '01',
    title: 'Upload Codebase',
    description: 'Provide any .zip archive or local directory. Decompressed safely in an isolated sandbox with Zip-Slip path validation.',
    tag: 'Ingestion Sandbox',
  },
  {
    step: '02',
    title: 'Analyze Architecture',
    description: 'Polyglot AST parsers map import hierarchies, evaluate file coupling, compute PageRank, and detect cycle loops.',
    tag: 'NetworkX Topology',
  },
  {
    step: '03',
    title: 'Predict Impact',
    description: 'Ensemble ML models predict downstream change impact probabilities and score dead code candidates.',
    tag: 'XGBoost & RF Inference',
  },
  {
    step: '04',
    title: 'Review Results',
    description: 'Inspect blast radiuses on the interactive dashboard and export formal compliance audit reports in PDF, Word, or CSV.',
    tag: 'Audit Reports & Export',
  },
];

const SUPPORTED_TECH = [
  { name: 'Python', ext: '.py', spec: 'AST Module Grammar' },
  { name: 'JavaScript', ext: '.js, .jsx', spec: 'ES6 & CommonJS Parser' },
  { name: 'TypeScript', ext: '.ts, .tsx', spec: 'Type-Aware AST Trees' },
  { name: 'HTML5', ext: '.html', spec: 'DOM Element Tree Model' },
  { name: 'CSS3', ext: '.css', spec: 'Selector & Rule Parser' },
];

export default function AboutPage() {
  const router = useRouter();

  const handleProceed = () => {
    localStorage.setItem('prevView', 'about');
    router.push('/upload');
  };

  const scrollToCapabilities = () => {
    document.getElementById('capabilities')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-[#080D1A] text-white flex flex-col selection:bg-indigo-500 selection:text-white">
      <Navbar currentView="about" />

      <main className="flex-1 w-full mx-auto px-6 sm:px-8 py-10 max-w-6xl">
        {/* =========================================================================
            1. HERO SECTION
        ========================================================================== */}
        <section className="text-center pt-6 pb-12 max-w-4xl mx-auto">
          {/* Eyebrow Badge */}
          <div className="inline-flex items-center gap-2 text-[10px] font-mono tracking-widest text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-3.5 py-1 rounded-full uppercase mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
            <span>ARCHITECTURE INTELLIGENCE &bull; OFFLINE SANDBOXED ML</span>
          </div>

          {/* Large Headline */}
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-[1.15] mb-5">
            Understand Your Codebase <br className="hidden sm:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-200 via-white to-indigo-300">
              Before You Change It.
            </span>
          </h1>

          {/* Supporting Text */}
          <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed mb-8">
            Analyze dependencies, predict downstream change impact, detect dead code, and understand architectural risk across your codebase with localized machine learning.
          </p>

          {/* CTA Actions */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 max-w-md mx-auto mb-14">
            <button
              onClick={handleProceed}
              className="w-full sm:w-auto flex-1 bg-[#4F46E5] hover:bg-[#4338CA] text-white text-xs sm:text-sm font-semibold py-3 px-6 rounded-xl transition-colors flex items-center justify-center gap-2 shadow-sm cursor-pointer"
            >
              <span>Analyze Your Codebase</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={scrollToCapabilities}
              className="w-full sm:w-auto bg-[#0E131F] hover:bg-[#161B28] text-slate-300 border border-white/10 text-xs sm:text-sm font-semibold py-3 px-6 rounded-xl transition-colors cursor-pointer"
            >
              Explore Capabilities
            </button>
          </div>

          {/* =========================================================================
              2. HERO PRODUCT VISUAL (DECORATIVE MOCKUP)
          ========================================================================== */}
          <div className="bg-[#0A0E1A] border border-white/[0.08] rounded-2xl p-5 sm:p-7 text-left shadow-2xl relative overflow-hidden mb-16">
            {/* Window Top Bar Chrome */}
            <div className="flex items-center justify-between border-b border-white/[0.06] pb-4 mb-6">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-rose-500/40 border border-rose-500/50"></span>
                <span className="w-3 h-3 rounded-full bg-amber-500/40 border border-amber-500/50"></span>
                <span className="w-3 h-3 rounded-full bg-emerald-500/40 border border-emerald-500/50"></span>
                <span className="text-[11px] font-mono text-slate-400 ml-2">impactx-graph-preview.tsx</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                  Simulation: Active
                </span>
                <span className="text-[10px] font-mono text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded">
                  XGBoost Confidence: 84.7%
                </span>
              </div>
            </div>

            {/* Simulated Dependency & Impact Graph Canvas */}
            <div className="py-2">
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider mb-4 flex items-center justify-between">
                <span>Topological Blast Radius Simulation</span>
                <span className="text-slate-400 lowercase">5 affected downstream entities</span>
              </div>

              {/* Node Hierarchy Visualization */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-3 items-center">
                {/* Level 1: Root Ingestion */}
                <div className="bg-[#0E131F] border border-white/10 rounded-xl p-3.5 space-y-1">
                  <div className="text-[10px] font-mono text-slate-400">01. INGESTION</div>
                  <div className="text-xs font-bold text-white truncate font-mono">dashboard.tsx</div>
                  <div className="text-[10px] text-slate-400 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                    <span>Client UI Entry</span>
                  </div>
                </div>

                {/* Level 2: Target File (Changed) */}
                <div className="bg-[#0E131F] border border-indigo-500/50 rounded-xl p-3.5 space-y-1 relative">
                  <span className="absolute -top-2 right-2 text-[9px] font-mono bg-indigo-600 text-white px-1.5 py-0.2 rounded font-bold uppercase">
                    Target File
                  </span>
                  <div className="text-[10px] font-mono text-indigo-300">02. MODIFIED</div>
                  <div className="text-xs font-bold text-white truncate font-mono">api_gateway.py</div>
                  <div className="text-[10px] text-indigo-300 flex items-center gap-1">
                    <Activity className="w-3 h-3 text-indigo-400" />
                    <span>PageRank: 0.142</span>
                  </div>
                </div>

                {/* Level 3: Direct Impact Components */}
                <div className="space-y-2">
                  <div className="bg-[#0E131F] border border-rose-500/30 rounded-xl p-2.5">
                    <div className="text-[9px] font-mono text-rose-400 font-semibold">DIRECT IMPACT (94%)</div>
                    <div className="text-xs font-bold text-white font-mono">auth_service.py</div>
                    <div className="text-[10px] text-slate-400">Hops: 1 &bull; In-Degree: 6</div>
                  </div>
                  <div className="bg-[#0E131F] border border-amber-500/30 rounded-xl p-2.5">
                    <div className="text-[9px] font-mono text-amber-400 font-semibold">DIRECT IMPACT (82%)</div>
                    <div className="text-xs font-bold text-white font-mono">user_service.py</div>
                    <div className="text-[10px] text-slate-400">Hops: 1 &bull; In-Degree: 4</div>
                  </div>
                </div>

                {/* Level 4: Transitive Ripple Components */}
                <div className="space-y-2">
                  <div className="bg-[#0E131F] border border-white/10 rounded-xl p-2.5">
                    <div className="text-[9px] font-mono text-slate-400">TRANSITIVE (76%)</div>
                    <div className="text-xs font-bold text-slate-200 font-mono">db_pool.py</div>
                    <div className="text-[10px] text-slate-400">Hops: 2 &bull; DB Connection</div>
                  </div>
                  <div className="bg-[#0E131F] border border-white/10 rounded-xl p-2.5">
                    <div className="text-[9px] font-mono text-slate-400">TRANSITIVE (42%)</div>
                    <div className="text-xs font-bold text-slate-200 font-mono">audit_logger.py</div>
                    <div className="text-[10px] text-slate-400">Hops: 2 &bull; Logging Queue</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Bottom Status Bar */}
            <div className="border-t border-white/[0.06] pt-3.5 mt-4 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400">
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span>Sandbox: Air-Gapped Offline</span>
                </span>
                <span>&bull;</span>
                <span>Zero Telemetry</span>
              </div>
              <div className="text-slate-400">
                NetworkX DiGraph &bull; 180 Edges &bull; 40 Vertices
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================================
            3. PRODUCT VALUE SECTION (3 DISTINCT CARDS)
        ========================================================================== */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <span className="text-[10px] font-mono tracking-widest text-slate-400 bg-white/[0.04] border border-white/10 px-3 py-1 rounded-full uppercase inline-block mb-3">
              PRIMARY VALUE
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Why Engineering Teams Use ImpactX
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Value Card 1 */}
            <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-7 flex flex-col justify-between hover:border-white/20 transition-all shadow-sm">
              <div>
                <div className="w-10 h-10 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400 mb-5">
                  <Zap className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2 tracking-tight">Change Impact Prediction</h3>
                <p className="text-xs text-slate-400 leading-relaxed mb-6">
                  Predict exactly which downstream components break when modifying a file. Pre-trained XGBoost models simulate multi-hop blast radiuses before PRs merge.
                </p>
              </div>
              <div className="pt-4 border-t border-white/[0.05] text-[11px] font-mono text-indigo-300 flex items-center gap-1.5">
                <span>Topological Traversal</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Value Card 2 */}
            <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-7 flex flex-col justify-between hover:border-white/20 transition-all shadow-sm">
              <div>
                <div className="w-10 h-10 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400 mb-5">
                  <Network className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2 tracking-tight">Architecture Intelligence</h3>
                <p className="text-xs text-slate-400 leading-relaxed mb-6">
                  Understand structural dependencies, in-degree coupling, and critical hubs. Detect circular dependency cycles before they destabilize your build.
                </p>
              </div>
              <div className="pt-4 border-t border-white/[0.05] text-[11px] font-mono text-indigo-300 flex items-center gap-1.5">
                <span>PageRank Centrality</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>

            {/* Value Card 3 */}
            <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-7 flex flex-col justify-between hover:border-white/20 transition-all shadow-sm">
              <div>
                <div className="w-10 h-10 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400 mb-5">
                  <CircleSlash className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2 tracking-tight">Dead Code Detection</h3>
                <p className="text-xs text-slate-400 leading-relaxed mb-6">
                  Catalog unreferenced classes, functions, and orphaned modules across repositories with confidence scoring powered by Random Forest classifiers.
                </p>
              </div>
              <div className="pt-4 border-t border-white/[0.05] text-[11px] font-mono text-indigo-300 flex items-center gap-1.5">
                <span>Confidence Scoring</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================================
            4. HOW IT WORKS SECTION (4-STAGE TIMELINE)
        ========================================================================== */}
        <section className="mb-20">
          <div className="text-center mb-10">
            <span className="text-[10px] font-mono tracking-widest text-slate-400 bg-white/[0.04] border border-white/10 px-3 py-1 rounded-full uppercase inline-block mb-3">
              PIPELINE WORKFLOW
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-2">
              How ImpactX Analyzes Your Code
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
              From raw repository archive to predictive graph intelligence in seconds.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {WORKFLOW_STEPS.map((item, idx) => (
              <div
                key={idx}
                className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-5 flex flex-col justify-between hover:border-white/20 transition-all shadow-sm"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-slate-300 bg-white/5 border border-white/10 px-2.5 py-1 rounded-md">
                      {item.step}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400">Stage {idx + 1}/4</span>
                  </div>
                  <h3 className="text-sm font-bold text-white mb-2">{item.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed mb-4">
                    {item.description}
                  </p>
                </div>
                <div>
                  <span className="text-[10px] font-mono text-slate-400 bg-white/[0.04] border border-white/[0.08] px-2 py-0.5 rounded-md inline-block">
                    {item.tag}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* =========================================================================
            5. CORE INTELLIGENCE CAPABILITIES (ID: capabilities)
        ========================================================================== */}
        <section id="capabilities" className="mb-20 scroll-mt-20">
          <div className="text-center mb-8">
            <span className="text-[10px] font-mono tracking-widest text-slate-400 bg-white/[0.04] border border-white/10 px-3 py-1 rounded-full uppercase inline-block mb-3">
              SYSTEM ARCHITECTURE
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-2">
              Core Intelligence Capabilities
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
              Six synchronized machine learning and graph engineering layers.
            </p>
          </div>

          {/* Balanced 3x2 Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {CAPABILITIES.map((cap, idx) => (
              <div
                key={idx}
                className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-6 flex flex-col justify-between hover:border-white/20 transition-all shadow-sm"
              >
                <div>
                  <div className="flex items-center mb-3">
                    <div className="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center mr-3 flex-shrink-0">
                      {cap.icon}
                    </div>
                    <h3 className="text-white font-bold text-sm tracking-tight">{cap.title}</h3>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed mb-5">
                    {cap.description}
                  </p>
                </div>
                <div>
                  <span className="text-[10px] font-mono text-slate-400 bg-white/[0.04] border border-white/[0.08] px-2.5 py-1 rounded-md inline-block">
                    {cap.tag}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* =========================================================================
            6. SECURITY & PRIVACY SECTION
        ========================================================================== */}
        <section className="mb-20">
          <div className="bg-[#0E131F] border border-white/[0.08] rounded-2xl p-8 sm:p-10 shadow-md">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-8 border-b border-white/[0.06] mb-8">
              <div>
                <span className="text-[10px] font-mono tracking-widest text-slate-400 bg-white/[0.04] border border-white/10 px-3 py-1 rounded-full uppercase inline-block mb-3">
                  SECURITY &bull; ZERO EXFILTRATION
                </span>
                <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
                  Enterprise-Grade Local Isolation
                </h2>
              </div>
              <div className="flex items-center gap-2 bg-[#080D1A] border border-white/10 px-3.5 py-2 rounded-xl text-xs font-mono text-emerald-400">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>100% Offline Sandboxing</span>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div>
                <div className="flex items-center gap-2 mb-2 text-white font-semibold text-xs sm:text-sm">
                  <Lock className="w-4 h-4 text-indigo-400" />
                  <span>Local Processing</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  All AST tokenization, graph computations, and ML inferences run completely inside your local environment.
                </p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2 text-white font-semibold text-xs sm:text-sm">
                  <ShieldCheck className="w-4 h-4 text-indigo-400" />
                  <span>Zero Telemetry</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Source code never leaves your workstation. No external API calls or telemetry are dispatched.
                </p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2 text-white font-semibold text-xs sm:text-sm">
                  <Layers className="w-4 h-4 text-indigo-400" />
                  <span>Sandboxed Execution</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Extracted repositories run in an isolated temporary directory that is cleansed immediately upon completion.
                </p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2 text-white font-semibold text-xs sm:text-sm">
                  <FileCheck2 className="w-4 h-4 text-indigo-400" />
                  <span>Zip-Slip Protection</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Strict directory traversal checks ensure files cannot unpack outside the allocated sandbox boundary.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================================
            7. SUPPORTED LANGUAGES SECTION
        ========================================================================== */}
        <section className="mb-20 text-center">
          <div className="mb-6">
            <span className="text-[10px] font-mono tracking-widest text-slate-400 bg-white/[0.04] border border-white/10 px-3 py-1 rounded-full uppercase inline-block mb-3">
              POLYGLOT PARSER ECOSYSTEM
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              Supported Codebase Technologies
            </h2>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 max-w-4xl mx-auto">
            {SUPPORTED_TECH.map((tech, idx) => (
              <div
                key={idx}
                className="bg-[#0E131F] border border-white/[0.08] rounded-xl p-4 text-center hover:border-white/20 transition-all shadow-sm"
              >
                <div className="text-sm font-bold text-white mb-0.5">{tech.name}</div>
                <div className="text-[11px] font-mono text-indigo-300 mb-1">{tech.ext}</div>
                <div className="text-[10px] text-slate-500">{tech.spec}</div>
              </div>
            ))}
          </div>
        </section>

        {/* =========================================================================
            8. FINAL CALL TO ACTION
        ========================================================================== */}
        <section className="bg-gradient-to-b from-[#0E131F] to-[#0A0E1A] border border-white/[0.08] rounded-2xl p-8 sm:p-12 text-center max-w-4xl mx-auto mb-16 shadow-lg">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-3">
            Ready to Understand Your Codebase?
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 max-w-lg mx-auto leading-relaxed mb-6">
            Analyze dependencies, identify architectural risks, and predict the impact of changes before they reach production.
          </p>
          <div className="max-w-xs mx-auto">
            <button
              onClick={handleProceed}
              className="w-full bg-[#4F46E5] hover:bg-[#4338CA] text-white text-xs sm:text-sm font-semibold py-3 px-6 rounded-xl transition-colors flex items-center justify-center gap-2 shadow-sm cursor-pointer"
            >
              <span>Analyze Your Codebase</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </section>

        {/* =========================================================================
            9. STRUCTURED FOOTER
        ========================================================================== */}
        <footer className="border-t border-white/[0.08] pt-12 pb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10 text-left">
            {/* Column 1: Brand */}
            <div>
              <div className="flex items-center space-x-2 mb-3">
                <span className="text-lg font-bold text-white font-mono">impactx</span>
                <span className="text-[9px] font-mono text-slate-400 bg-white/5 border border-white/10 px-1.5 py-0.5 rounded">v2.1</span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-4">
                Enterprise Code Change Impact &amp; Architecture Intelligence Platform. 100% offline sandboxed ML.
              </p>
              <div className="text-[11px] text-slate-400 font-mono">
                &copy; {new Date().getFullYear()} ImpactX Engine
              </div>
            </div>

            {/* Column 2: Platform */}
            <div>
              <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3 font-mono">Platform</h4>
              <ul className="space-y-2 text-xs text-slate-400">
                <li>Change Impact Prediction</li>
                <li>Dependency Graph Topology</li>
                <li>Dead Code Detection</li>
                <li>Executive Audit Reports</li>
              </ul>
            </div>

            {/* Column 3: Security */}
            <div>
              <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3 font-mono">Security</h4>
              <ul className="space-y-2 text-xs text-slate-400">
                <li>Local Processing Only</li>
                <li>Zero Telemetry</li>
                <li>Zip-Slip Protection</li>
                <li>Isolated Temp Sandboxing</li>
              </ul>
            </div>

            {/* Column 4: Architecture */}
            <div>
              <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3 font-mono">Engine</h4>
              <ul className="space-y-2 text-xs text-slate-400">
                <li>XGBoost Classifier</li>
                <li>Random Forest Scorer</li>
                <li>NetworkX Graph Engine</li>
                <li>Multi-Language AST Parsers</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-white/[0.05] pt-6 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-400 font-mono">
            <div>ImpactX &bull; Architecture Intelligence &bull; Offline ML</div>
            <div className="mt-2 sm:mt-0">Local Sandboxed Execution Ready</div>
          </div>
        </footer>
      </main>
    </div>
  );
}
