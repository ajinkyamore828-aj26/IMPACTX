'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { BarChart3, FolderTree, Zap, FileSearch, Brain, FileText } from 'lucide-react';
import Navbar from '@/components/Navbar';
import MetricCard from '@/components/MetricCard';
import Expander from '@/components/Expander';
import DataTable from '@/components/DataTable';
import MultiSelect from '@/components/MultiSelect';
import LanguagePie from '@/components/charts/LanguagePie';
import RocCurve from '@/components/charts/RocCurve';
import FeatureImportanceBar from '@/components/charts/FeatureImportanceBar';
import ConfusionMatrix from '@/components/charts/ConfusionMatrix';
import { loadSession, clearSession } from '@/lib/store';
import { SessionData, getImpact, getAiArch, getAiImpact, getAiUnused, getModelsMeta, exportReport } from '@/lib/api';

const TABS = [
  { id: 'overview', label: 'Overview & Metrics', icon: BarChart3 },
  { id: 'structure', label: 'Project Structure', icon: FolderTree },
  { id: 'impact', label: 'Impact Analysis', icon: Zap },
  { id: 'deadcode', label: 'Dead Code', icon: FileSearch },
  { id: 'explainability', label: 'ML Explainability', icon: Brain },
  { id: 'reports', label: 'Audit Reports', icon: FileText }
];

const RISK_OPTIONS = [
  { id: 'CRITICAL', label: 'CRITICAL' },
  { id: 'HIGH', label: 'HIGH' },
  { id: 'MEDIUM', label: 'MEDIUM' },
  { id: 'LOW', label: 'LOW' }
];

const TYPE_OPTIONS = [
  { id: 'file', label: 'file' },
  { id: 'function', label: 'function' },
  { id: 'class', label: 'class' }
];

function parseEntityLabel(entityId: string) {
  const clean = (entityId || '').replace(/\\/g, '/');
  const parts = clean.split('/');
  const lastPart = parts[parts.length - 1] || entityId;
  const hasExt = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.html', '.css'].some(ext => lastPart.endsWith(ext));
  if (hasExt) {
    return { name: lastPart, path: clean };
  } else {
    return { name: lastPart, path: parts.slice(0, -1).join('/') || clean };
  }
}

export default function DashboardPage() {
  const router = useRouter();
  const [isClient, setIsClient] = useState(false);
  const [session, setSession] = useState<{ sessionId: string; data: SessionData } | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  // AI responses state
  const [aiArch, setAiArch] = useState<{ content: string; loading: boolean }>({ content: '', loading: false });
  const [aiImpact, setAiImpact] = useState<{ content: string; loading: boolean }>({ content: '', loading: false });
  const [aiUnused, setAiUnused] = useState<{ content: string; loading: boolean }>({ content: '', loading: false });

  // Tab specific state
  const [structSearch, setStructSearch] = useState('');
  const [structLang, setStructLang] = useState('All');

  const [selectedHubIdx, setSelectedHubIdx] = useState(0);

  const [selectedComponent, setSelectedComponent] = useState('');
  const [impactData, setImpactData] = useState<any>(null);
  const [impactLoading, setImpactLoading] = useState(false);
  const [impactError, setImpactError] = useState('');

  const [unusedRiskFilter, setUnusedRiskFilter] = useState<string[]>(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']);
  const [unusedTypeFilter, setUnusedTypeFilter] = useState<string[]>(['file', 'function', 'class']);
  const [selectedDeadCodeItem, setSelectedDeadCodeItem] = useState('');

  const [modelsMeta, setModelsMeta] = useState<any>(null);

  // Tab 6: Reports & Export state
  const [exportingFormat, setExportingFormat] = useState<string | null>(null);
  const [exportSuccessMsg, setExportSuccessMsg] = useState<string | null>(null);
  const [exportErrorMsg, setExportErrorMsg] = useState<string | null>(null);
  const [reportPreviewTab, setReportPreviewTab] = useState<'summary' | 'json' | 'template'>('summary');
  const [copiedJson, setCopiedJson] = useState(false);

  useEffect(() => {
    setIsClient(true);
    const s = loadSession();
    if (!s || !s.data) {
      router.push('/upload');
    } else {
      setSession(s);
      let initialComp = '';
      if (s.data.top_hubs && s.data.top_hubs.length > 0) {
        initialComp = s.data.top_hubs[0].id;
      } else if (s.data.graph_nodes && s.data.graph_nodes.length > 0) {
        initialComp = s.data.graph_nodes[0].id;
      }
      setSelectedComponent(initialComp);
    }
  }, [router]);

  useEffect(() => {
    if (activeTab === 'explainability' && !modelsMeta) {
      getModelsMeta().then(setModelsMeta).catch(console.error);
    }
  }, [activeTab, modelsMeta]);

  useEffect(() => {
    if (session && selectedComponent) {
      handleImpactSelect(selectedComponent);
    }
  }, [selectedComponent, session?.sessionId]);

  const handleImpactSelect = async (comp: string) => {
    if (!comp || !session) return;
    setImpactLoading(true);
    setImpactError('');
    setAiImpact({ content: '', loading: false });
    try {
      const res = await getImpact(session.sessionId, comp, {
        graph_nodes: session.data.graph_nodes,
        graph_edges: session.data.graph_edges,
      });
      setImpactData(res);
    } catch (e: any) {
      console.error('Impact query error:', e);
      setImpactError(e.message || 'Failed to analyze impact');
    } finally {
      setImpactLoading(false);
    }
  };

  if (!isClient || !session || !session.data) {
    return (
      <div className="min-h-screen bg-bg-page flex items-center justify-center text-slate-400">
        <div className="animate-pulse">Loading dashboard...</div>
      </div>
    );
  }

  const { data, sessionId } = session;
  const scanInfo = data.scan_info || {};
  const projectName = scanInfo.project_name || 'task2';
  const files = scanInfo.files || [];
  const topHubs = data.top_hubs || [];
  const unusedResults = data.unused_results || [];
  const graphNodes = data.graph_nodes || [];
  const graphEdges = data.graph_edges || [];
  const cycles = data.cycles || [];
  const hasCycles = Boolean(data.has_cycles);
  const languageDist = scanInfo.language_distribution || {};

  const totalFiles = scanInfo.total_files || files.length || 0;
  const totalLoc = scanInfo.total_code_lines || 0;
  const totalLines = scanInfo.total_lines || totalLoc;
  const totalNodes = graphNodes.length;
  const totalEdges = graphEdges.length;
  const avgCoupling = totalNodes > 0 ? (totalEdges / totalNodes).toFixed(2) : '0.00';
  const maxInDegree = topHubs.length > 0 ? Math.max(...topHubs.map((h: any) => h.in_degree || 0)) : 0;
  const highRiskDeadCode = unusedResults.filter((u: any) => u.risk_level === 'HIGH' || u.risk_level === 'CRITICAL').length;

  const handleAiArch = async () => {
    setAiArch({ content: '', loading: true });
    try {
      const res = await getAiArch(sessionId);
      setAiArch({ content: res.content || 'No assessment generated.', loading: false });
    } catch (e: any) {
      setAiArch({ content: `AI Error: ${e.message || 'Failed to generate assessment'}`, loading: false });
    }
  };

  const handleAiImpact = async () => {
    if (!selectedComponent || !impactData) return;
    setAiImpact({ content: '', loading: true });
    try {
      const res = await getAiImpact(sessionId, selectedComponent, impactData);
      setAiImpact({ content: res.content || 'No impact advisory generated.', loading: false });
    } catch (e: any) {
      setAiImpact({ content: `AI Error: ${e.message || 'Failed to reason impact'}`, loading: false });
    }
  };

  const handleAiUnused = async () => {
    setAiUnused({ content: '', loading: true });
    try {
      const res = await getAiUnused(sessionId, unusedResults, {
        risk_levels: unusedRiskFilter,
        entity_types: unusedTypeFilter
      });
      setAiUnused({ content: res.content || 'No dead code advisory generated.', loading: false });
    } catch (e: any) {
      setAiUnused({ content: `AI Error: ${e.message || 'Failed to generate dead code advisory'}`, loading: false });
    }
  };

  const handleExport = async (format: 'pdf' | 'docx' | 'csv' | 'html' | 'json') => {
    if (exportingFormat) return;
    setExportingFormat(format);
    setExportSuccessMsg(null);
    setExportErrorMsg(null);
    try {
      const fallbackData = {
        scan_info: {
          project_name: projectName,
          total_files: totalFiles,
          total_code_lines: totalLoc,
          total_lines: totalLines,
          language_distribution: languageDist,
          files: files,
          timestamp: scanInfo.timestamp || new Date().toISOString(),
        },
        top_hubs: topHubs,
        unused_results: unusedResults,
        graph_nodes: graphNodes,
        graph_edges: graphEdges,
        has_cycles: hasCycles,
        cycles: cycles,
      };
      const blob = await exportReport(sessionId, format, fallbackData);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const safeName = (projectName || 'project').replace(/[^a-zA-Z0-9_-]/g, '_');
      const ext = format;
      a.download = `impactx_audit_report_${safeName}.${ext}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      setExportSuccessMsg(`Successfully generated and downloaded ${format.toUpperCase()} report.`);
      setTimeout(() => setExportSuccessMsg(null), 6000);
    } catch (e: any) {
      setExportErrorMsg(e.message || `Failed to export ${format.toUpperCase()} report.`);
    } finally {
      setExportingFormat(null);
    }
  };

  const copyJsonToClipboard = () => {
    const manifest = {
      project: projectName,
      timestamp: scanInfo.timestamp || new Date().toISOString(),
      health_score: healthScore,
      total_files: totalFiles,
      total_code_lines: totalLoc,
      dependencies_count: totalEdges,
      dead_code_candidates: unusedResults.length,
      circular_dependencies: cycles.length,
      top_hubs_count: topHubs.length,
    };
    navigator.clipboard.writeText(JSON.stringify(manifest, null, 2));
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 3000);
  };

  // Calculate architectural health score
  const critDeadCount = unusedResults.filter((u: any) => String(u.risk_level || '').toUpperCase() === 'CRITICAL').length;
  const highDeadCount = unusedResults.filter((u: any) => String(u.risk_level || '').toUpperCase() === 'HIGH').length;
  let penalty = 0;
  if (hasCycles) penalty += 25 + Math.min(15, cycles.length * 5);
  penalty += Math.min(25, critDeadCount * 4);
  penalty += Math.min(15, highDeadCount * 2);
  const healthScore = Math.max(15, 100 - penalty);

  const activeHub = topHubs[selectedHubIdx] || topHubs[0];
  const activeHubMeta = activeHub ? parseEntityLabel(activeHub.id) : null;
  const selectedCompLabel = parseEntityLabel(selectedComponent);

  return (
    <div className="min-h-screen bg-bg-page text-white flex flex-col">
      <Navbar currentView="dashboard" projectName={projectName} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-6">
        {/* Top HUD Sub-Header */}
        <div className="flex items-center justify-between gap-4 mb-6">
          <button
            onClick={() => { clearSession(); router.push('/upload'); }}
            className="bg-[#161B28] hover:bg-[#1E2538] text-slate-300 text-xs px-4 py-2.5 rounded-lg border border-white/10 font-medium transition-colors flex-shrink-0 shadow-sm"
          >
            Back to Upload
          </button>
          <div className="bg-[#0D1220] border border-white/10 rounded-xl px-5 py-2.5 flex items-center justify-between flex-1 shadow-sm">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span className="text-xs font-bold text-white">Active Codebase: {projectName}</span>
            </div>
            <div className="text-xs text-slate-400 font-medium">
              {totalFiles} Files • {totalLoc.toLocaleString()} Lines of Code • {totalNodes} Graph Entities • {totalEdges} Dependencies
            </div>
          </div>
        </div>

        {/* Segmented Toolbar Navigation Tabs */}
        <div className="bg-[#0D1220] border border-white/10 rounded-xl p-1.5 flex gap-2 mb-8 shadow-sm">
          {TABS.map(t => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex-1 py-2.5 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                activeTab === t.id
                  ? 'bg-[#4F46E5] text-white shadow-md'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <t.icon className="w-4 h-4" />
              <span>{t.label}</span>
            </button>
          ))}
        </div>

        {/* TAB 1: OVERVIEW & METRICS */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-white tracking-tight mb-4">
              Project Overview: <span className="text-white">{projectName}</span>
            </h2>

            {/* 4 Metric Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <MetricCard title="TOTAL FILES" value={totalFiles} subtext="Analyzed in codebase" />
              <MetricCard title="LINES OF CODE" value={totalLoc.toLocaleString()} subtext={`Total lines: ${totalLines.toLocaleString()}`} />
              <MetricCard title="DEPENDENCIES" value={totalEdges} subtext={`Entities mapped: ${totalNodes}`} />
              <MetricCard title="DEAD CODE CANDIDATES" value={unusedResults.length} subtext={`High Risk: ${highRiskDeadCode}`} />
            </div>

            {/* Row 2: Donut Chart + Architectural Coupling */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Language Composition */}
              <div className="glass-card p-6 flex flex-col justify-between">
                <h3 className="text-sm font-bold text-white mb-2 uppercase tracking-wider text-slate-400">
                  Language Composition
                </h3>
                <div className="h-[280px] flex items-center justify-center">
                  <LanguagePie langDist={languageDist} />
                </div>
              </div>

              {/* Architectural Coupling & Health */}
              <div className="glass-card p-6 flex flex-col justify-between">
                <h3 className="text-sm font-bold text-white mb-4 uppercase tracking-wider text-slate-400">
                  Architectural Coupling &amp; Health
                </h3>
                <div className="grid grid-cols-2 gap-4 h-full">
                  <div className="bg-[#080D1A] border border-white/5 rounded-xl p-4 flex flex-col justify-center">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">GRAPH ENTITIES</div>
                    <div className="text-3xl font-extrabold text-white">{totalNodes}</div>
                    <div className="text-[11px] text-slate-500 mt-1">Total components mapped</div>
                  </div>
                  <div className="bg-[#080D1A] border border-white/5 rounded-xl p-4 flex flex-col justify-center">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">AVG COUPLING</div>
                    <div className="text-3xl font-extrabold text-white">{avgCoupling}</div>
                    <div className="text-[11px] text-slate-500 mt-1">Dependencies per entity</div>
                  </div>
                  <div className="bg-[#080D1A] border border-white/5 rounded-xl p-4 flex flex-col justify-center">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">MAX IN-DEGREE</div>
                    <div className="text-3xl font-extrabold text-white">{maxInDegree}</div>
                    <div className="text-[11px] text-slate-500 mt-1">Peak dependents on single component</div>
                  </div>
                  <div className="bg-[#080D1A] border border-white/5 rounded-xl p-4 flex flex-col justify-center">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">CYCLES</div>
                    <div className={`text-2xl font-extrabold ${hasCycles ? 'text-red-400' : 'text-white'}`}>
                      {hasCycles ? `${cycles.length} Detected` : '0 (Clean DAG)'}
                    </div>
                    <div className="text-[11px] text-slate-500 mt-1">Circular dependency count</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Expander 1: AI Architectural Assessment */}
            <Expander title="Groq AI Architectural Assessment & Risk Intelligence" defaultOpen={true}>
              <p className="text-xs text-slate-400 mb-3">
                Generate an executive architectural assessment, hotspot risk analysis, and change isolation recommendations.
              </p>
              {!aiArch.content && !aiArch.loading ? (
                <button
                  onClick={handleAiArch}
                  className="bg-[#1E2538] hover:bg-[#2A344D] text-white border border-white/10 text-xs px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Generate AI Architectural Intelligence
                </button>
              ) : aiArch.loading ? (
                <div className="text-xs text-indigo-400 animate-pulse py-2">
                  Generating executive architectural assessment with Groq Llama3...
                </div>
              ) : (
                <div className="ai-response pt-2">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{aiArch.content}</ReactMarkdown>
                  <button
                    onClick={handleAiArch}
                    className="bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 text-xs px-3 py-1.5 rounded-md mt-4 transition-colors"
                  >
                    Re-generate Assessment
                  </button>
                </div>
              )}
            </Expander>

            {/* Expander 2: Top Architectural Hubs */}
            <Expander title="Top Architectural Hubs (Highest Risk Components)" defaultOpen={true}>
              <p className="text-xs text-slate-400 mb-4">
                Components with highest PageRank centrality and incoming dependents. Changes to these components produce the largest downstream ripple effect.
              </p>

              {topHubs.length > 0 ? (
                <div className="space-y-4">
                  {/* Hub Selection Row */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
                    <div className="md:col-span-2">
                      <label className="block text-[11px] font-bold text-slate-400 uppercase mb-1.5">
                        Inspect Specific Hub from Dropdown:
                      </label>
                      <select
                        value={selectedHubIdx}
                        onChange={e => setSelectedHubIdx(Number(e.target.value))}
                        className="w-full bg-[#080D1A] border border-white/10 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                      >
                        {topHubs.map((h: any, i: number) => {
                          const lbl = parseEntityLabel(h.id);
                          return (
                            <option key={h.id} value={i}>
                              {lbl.name} ({String(h.entity_type || 'file').toUpperCase()}) | In-Dependents: {h.in_degree || 0}
                            </option>
                          );
                        })}
                      </select>
                    </div>

                    <div className="bg-[#080D1A] border border-white/10 rounded-lg p-3 text-right">
                      <div className="text-[10px] font-bold text-slate-400 uppercase">PageRank Centrality</div>
                      <div className="text-lg font-bold text-white">
                        {(activeHub?.pagerank || 0).toFixed(4)}
                      </div>
                    </div>
                  </div>

                  {/* Active Hub Card */}
                  {activeHub && activeHubMeta && (
                    <div className="bg-[#080D1A] border border-white/10 rounded-xl p-4 flex items-center justify-between flex-wrap gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-bold text-white">{activeHubMeta.name}</span>
                          <span className="text-[10px] font-mono bg-white/5 text-slate-400 border border-white/10 px-2 py-0.5 rounded uppercase">
                            {activeHub.entity_type || 'file'}
                          </span>
                        </div>
                        <div className="text-xs text-slate-500 font-mono">{activeHubMeta.path}</div>
                      </div>
                      <div className="flex gap-4">
                        <div className="text-center bg-white/5 border border-white/5 rounded-lg px-4 py-1.5">
                          <div className="text-[9px] font-bold text-slate-400 uppercase">INCOMING</div>
                          <div className="text-lg font-bold text-white">{activeHub.in_degree || 0}</div>
                        </div>
                        <div className="text-center bg-white/5 border border-white/5 rounded-lg px-4 py-1.5">
                          <div className="text-[9px] font-bold text-slate-400 uppercase">OUTGOING</div>
                          <div className="text-lg font-bold text-white">{activeHub.out_degree || 0}</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Hubs Data Table */}
                  <div className="glass-card overflow-hidden">
                    <DataTable
                      columns={[
                        { key: 'component', label: 'Component' },
                        { key: 'type', label: 'Type' },
                        { key: 'pagerank', label: 'PageRank' },
                        { key: 'in_degree', label: 'In-Dependents (In)' },
                        { key: 'out_degree', label: 'Dependencies (Out)' },
                        { key: 'file_path', label: 'File Location' }
                      ]}
                      rows={topHubs.map((h: any) => {
                        const lbl = parseEntityLabel(h.id);
                        return {
                          component: lbl.name,
                          type: String(h.entity_type || 'file').toUpperCase(),
                          pagerank: (h.pagerank || 0).toFixed(4),
                          in_degree: h.in_degree || 0,
                          out_degree: h.out_degree || 0,
                          file_path: lbl.path
                        };
                      })}
                    />
                  </div>
                </div>
              ) : (
                <div className="text-xs text-slate-500">No architectural hubs detected.</div>
              )}
            </Expander>
          </div>
        )}

        {/* TAB 2: PROJECT STRUCTURE */}
        {activeTab === 'structure' && (() => {
          const detectedLangs = ['All', ...Object.keys(languageDist)];
          const filteredFiles = files.filter((f: any) => {
            if (structLang !== 'All' && f.language !== structLang) return false;
            if (structSearch && !f.path.toLowerCase().includes(structSearch.toLowerCase())) return false;
            return true;
          });

          return (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white tracking-tight mb-1">
                  Project File Inventory &amp; AST Breakdown
                </h2>
                <p className="text-xs text-slate-400">
                  Complete breakdown of source files, lines of code, and architectural categories.
                </p>
              </div>

              {/* 3 Metric Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <MetricCard title="REPOSITORY FILES" value={files.length} subtext="Source files cataloged" />
                <MetricCard title="CODE LINES (LOC)" value={totalLoc.toLocaleString()} subtext="Effective code lines" />
                <MetricCard title="LANGUAGES DETECTED" value={Object.keys(languageDist).length} subtext="Multi-language AST parsers" />
              </div>

              {/* Search & Filter Row */}
              <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="w-full md:flex-1">
                  <label className="block text-[11px] font-bold text-slate-400 uppercase mb-1.5">
                    Search files by path or name:
                  </label>
                  <input
                    type="text"
                    value={structSearch}
                    onChange={e => setStructSearch(e.target.value)}
                    placeholder="Search by file path or entity name..."
                    className="w-full bg-[#080D1A] border border-white/10 rounded-lg px-4 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="w-full md:w-56">
                  <label className="block text-[11px] font-bold text-slate-400 uppercase mb-1.5">
                    Filter by language:
                  </label>
                  <select
                    value={structLang}
                    onChange={e => setStructLang(e.target.value)}
                    className="w-full bg-[#080D1A] border border-white/10 rounded-lg px-3 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
                  >
                    {detectedLangs.map(l => <option key={l} value={l}>{l}</option>)}
                  </select>
                </div>
              </div>

              {/* Files Table */}
              <div className="glass-card overflow-hidden">
                <div className="max-h-[600px] overflow-y-auto">
                  <DataTable
                    columns={[
                      { key: 'path', label: 'File Path' },
                      { key: 'language', label: 'Language' },
                      { key: 'category', label: 'Category' },
                      { key: 'code_lines', label: 'Code LOC' },
                      { key: 'total_lines', label: 'Total Lines' },
                      { key: 'size', label: 'File Size' }
                    ]}
                    rows={filteredFiles.map((f: any) => ({
                      path: f.path,
                      language: f.language || 'Unknown',
                      category: String(f.category || 'code').toUpperCase(),
                      code_lines: f.code_lines || 0,
                      total_lines: f.total_lines || 0,
                      size: `${((f.size_bytes || 0) / 1024).toFixed(1)} KB`
                    }))}
                  />
                </div>
              </div>
            </div>
          );
        })()}

        {/* TAB 3: IMPACT ANALYSIS */}
        {activeTab === 'impact' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-white tracking-tight mb-1">
                Change Impact &amp; Blast Radius Prediction
              </h2>
              <p className="text-xs text-slate-400">
                Select a component to predict downstream blast radius, transitive affected entities, and ML risk scores.
              </p>
            </div>

            {/* Selection Area Card */}
            <div className="glass-card p-6">
              {topHubs.length > 0 && (
                <div className="mb-5">
                  <div className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider mb-2.5">
                    RECOMMENDED HIGH-IMPACT HUBS (HIGHEST BLAST RADIUS):
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {topHubs.slice(0, 5).map((h: any) => {
                      const lbl = parseEntityLabel(h.id);
                      const isSelected = selectedComponent === h.id;
                      return (
                        <button
                          key={h.id}
                          onClick={() => {
                            setSelectedComponent(h.id);
                            handleImpactSelect(h.id);
                          }}
                          className={`text-xs px-3.5 py-1.5 rounded-lg border transition-all ${
                            isSelected
                              ? 'bg-[#4F46E5] border-indigo-400 text-white font-semibold shadow-sm'
                              : 'bg-white/5 border-white/10 text-slate-300 hover:bg-white/10'
                          }`}
                        >
                          {lbl.name} ({h.in_degree || 0} refs)
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
                  SELECT TARGET COMPONENT TO MODIFY:
                </label>
                <select
                  value={selectedComponent}
                  onChange={e => {
                    setSelectedComponent(e.target.value);
                    handleImpactSelect(e.target.value);
                  }}
                  className="w-full bg-[#080D1A] border border-white/10 rounded-lg px-4 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500 font-mono"
                >
                  <option value="">-- Choose a component --</option>
                  {graphNodes.map((n: any) => <option key={n.id} value={n.id}>{n.id}</option>)}
                </select>
              </div>
            </div>

            {impactLoading && (
              <div className="glass-card p-6 text-center text-xs text-indigo-400 animate-pulse">
                Calculating blast radius &amp; ML probability cascade...
              </div>
            )}

            {impactError && (
              <div className="bg-red-950/40 border border-red-500/30 rounded-xl p-4 text-xs text-red-300 flex items-center justify-between">
                <span>Error computing impact: {impactError}</span>
                <button
                  onClick={() => handleImpactSelect(selectedComponent)}
                  className="px-3 py-1 bg-red-900/50 hover:bg-red-800 text-white rounded text-xs transition-colors"
                >
                  Retry
                </button>
              </div>
            )}

            {impactData && !impactLoading && (
              <div className="space-y-6">
                {/* 5 Metric Cards */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <MetricCard title="BLAST RADIUS" value={impactData.total_affected || 0} subtext="Downstream components" />
                  <MetricCard title="DIRECT (LEVEL 1)" value={impactData.direct_count || 0} subtext="Immediate dependents" />
                  <MetricCard title="TRANSITIVE (LEVEL 2+)" value={impactData.indirect_count || 0} subtext="Cascade ripple" />
                  <MetricCard title="HIGH RISK" value={impactData.high_risk_count || 0} subtext="Probability >= 70%" />
                  <MetricCard title="PREREQUISITES" value={impactData.upstream_count || (impactData.upstream_dependencies?.length || 0)} subtext="Required upstream dependencies" />
                </div>

                {/* Downstream Blast Radius Table or Zero-Blast Info */}
                {impactData.affected_components && impactData.affected_components.length > 0 ? (
                  <>
                    {/* Downstream Blast Radius Dropdown Expander */}
                    <Expander title={`Downstream Blast Radius (${impactData.total_affected} Affected Components)`} defaultOpen={true}>
                      <div className="border border-white/10 rounded-lg overflow-hidden bg-[#0A0E1A]">
                        <div className="max-h-[420px] overflow-y-auto">
                          <DataTable
                            columns={[
                              { key: 'name', label: 'Affected Component' },
                              { key: 'type', label: 'Type' },
                              { key: 'level', label: 'Impact Level' },
                              { key: 'distance', label: 'Distance' },
                              { key: 'probability', label: 'Impact Probability' },
                              { key: 'risk_level', label: 'Risk Tier' },
                              { key: 'driver', label: 'Key Driver' },
                              { key: 'file_path', label: 'File Location' }
                            ]}
                            rows={impactData.affected_components.map((a: any) => ({
                              name: parseEntityLabel(a.component).name,
                              type: String(a.type || 'file').toUpperCase(),
                              level: a.level || (a.distance === 1 ? 'Direct (Level 1)' : `Transitive (Level ${a.distance || 2})`),
                              distance: a.distance || 1,
                              probability: a.probability || 0,
                              risk_level: (
                                <span className="bg-[#854D0E]/40 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded text-[10px] font-bold">
                                  {a.risk_level || 'HIGH'}
                                </span>
                              ),
                              driver: (a.explanations && a.explanations[0]) || (a.distance === 1 ? 'Direct syntactic dependency chain' : `Transitive dependency chain of length ${a.distance || 2}`),
                              file_path: a.file_path || parseEntityLabel(a.component).path
                            }))}
                            progressColumn="probability"
                          />
                        </div>
                      </div>
                    </Expander>

                    {/* Dependency Ripple Paths Dropdown Expander */}
                    <Expander title={`Dependency Ripple Paths (${impactData.affected_components.length} Chains)`} defaultOpen={true}>
                      <div className="space-y-2 max-h-[380px] overflow-y-auto pr-1">
                        {impactData.affected_components.map((aff: any, idx: number) => {
                          const fullPath = aff.file_path || aff.component;
                          const levelLabel = aff.level || (aff.distance === 1 ? 'Direct (Level 1)' : `Transitive (Level ${aff.distance || 2})`);
                          const pathArray = aff.path && aff.path.length > 0 ? aff.path : [selectedComponent, aff.component];
                          return (
                            <div key={idx} className="bg-[#080D1A] border border-white/10 rounded-lg p-3 flex items-center justify-between flex-wrap gap-2 text-xs hover:border-indigo-500/30 transition-colors">
                              <div className="text-slate-300 font-mono text-[11px]">
                                <span className="text-white font-medium">{fullPath}</span>
                                <span className="text-indigo-400 ml-1.5">({levelLabel}):</span>
                              </div>
                              <div className="bg-white/5 border border-white/10 rounded px-2.5 py-1 text-[11px] font-mono text-indigo-300 flex items-center gap-2">
                                {pathArray.join(' ➔ ')}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </Expander>
                  </>
                ) : (
                  <div className="bg-[#0E131F] border border-white/10 rounded-xl p-5 text-xs text-slate-300 leading-relaxed">
                    <span className="text-amber-400 font-semibold mr-1.5">Terminal Component:</span>
                    No downstream components depend on <code className="text-indigo-300">{selectedComponent}</code> (Blast Radius = 0). Changes to this file will not break other files in the codebase.
                  </div>
                )}

                {/* Upstream Prerequisites Table */}
                {impactData.upstream_dependencies && impactData.upstream_dependencies.length > 0 && (
                  <div className="glass-card overflow-hidden">
                    <div className="px-6 py-4 border-b border-white/10 bg-white/[0.02]">
                      <h3 className="text-sm font-bold text-white tracking-wide flex items-center gap-2">
                        Upstream Prerequisites ({impactData.upstream_dependencies.length} components required by{' ' }
                        <span className="px-2 py-0.5 rounded bg-white/10 font-mono text-white text-xs border border-white/10">
                          {selectedCompLabel.name}
                        </span>
                        )
                      </h3>
                    </div>
                    <div className="max-h-[300px] overflow-y-auto">
                      <DataTable
                        columns={[
                          { key: 'component', label: 'Prerequisite Component' },
                          { key: 'type', label: 'Type' },
                          { key: 'language', label: 'Language' },
                          { key: 'relationship', label: 'Relationship' }
                        ]}
                        rows={impactData.upstream_dependencies.map((u: any) => ({
                          component: u.component,
                          type: String(u.type || 'file').toUpperCase(),
                          language: u.language || 'JavaScript',
                          relationship: u.relationship || 'imports'
                        }))}
                      />
                    </div>
                  </div>
                )}

                {/* Expander: Groq AI Semantic Blast Radius */}
                <Expander title={`Groq AI Semantic Blast Radius & Verification: ${selectedCompLabel.name}`}>
                  {!aiImpact.content && !aiImpact.loading ? (
                    <div>
                      <p className="text-xs text-slate-400 mb-3">
                        Analyze downstream consumer breakage and recommend targeted regression tests with Groq AI.
                      </p>
                      <button
                        onClick={handleAiImpact}
                        className="bg-[#1E2538] hover:bg-[#2A344D] text-white border border-white/10 text-xs px-4 py-2 rounded-lg font-medium transition-colors"
                      >
                        Reason Blast Radius with Groq AI
                      </button>
                    </div>
                  ) : aiImpact.loading ? (
                    <div className="text-xs text-indigo-400 animate-pulse py-2">
                      Analyzing semantic blast radius for {selectedCompLabel.name}...
                    </div>
                  ) : (
                    <div className="ai-response pt-2">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{aiImpact.content}</ReactMarkdown>
                      <button
                        onClick={handleAiImpact}
                        className="bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 text-xs px-3 py-1.5 rounded-md mt-4 transition-colors"
                      >
                        Re-analyze Blast Radius
                      </button>
                    </div>
                  )}
                </Expander>
              </div>
            )}
          </div>
        )}

        {/* TAB 4: DEAD CODE */}
        {activeTab === 'deadcode' && (() => {
          const filteredUnused = unusedResults.filter((u: any) => {
            if (!unusedRiskFilter.includes(u.risk_level)) return false;
            const t = String(u.type || 'file').toLowerCase();
            if (!unusedTypeFilter.includes(t)) return false;
            return true;
          });

          return (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-white tracking-tight mb-1">
                  Dead Code &amp; Unreferenced Entity Detection
                </h2>
                <p className="text-xs text-slate-400">
                  Components with zero or minimal incoming references evaluated with graph PageRank and machine learning non-use confidence scores.
                </p>
              </div>

              {/* Filters Row: Exactly matching Streamlit UI */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <MultiSelect
                  label="Filter by Risk Tier"
                  hasHelp={true}
                  helpText="Only show candidates at or above selected risk tier"
                  options={RISK_OPTIONS}
                  selected={unusedRiskFilter}
                  onChange={setUnusedRiskFilter}
                />
                <MultiSelect
                  label="Filter by Entity Type"
                  options={TYPE_OPTIONS}
                  selected={unusedTypeFilter}
                  onChange={setUnusedTypeFilter}
                />
              </div>

              {/* Quick Component Dropdown Selector */}
              <div className="glass-card p-5">
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
                  INSPECT CANDIDATE FROM DROPDOWN:
                </label>
                <select
                  value={selectedDeadCodeItem}
                  onChange={e => setSelectedDeadCodeItem(e.target.value)}
                  className="w-full bg-[#080D1A] border border-white/10 rounded-lg px-4 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500 font-mono"
                >
                  <option value="">-- Select candidate from dropdown ({filteredUnused.length} available) --</option>
                  {filteredUnused.map((u: any, idx: number) => {
                    const compId = u.entity_id || u.name;
                    const risk = u.risk_level || 'HIGH';
                    const prob = ((u.unused_probability || 0) * 100).toFixed(1);
                    return (
                      <option key={idx} value={compId}>
                        {compId} [{risk} | {prob}% confidence | {u.reference_count || 0} refs]
                      </option>
                    );
                  })}
                </select>

                {selectedDeadCodeItem && (() => {
                  const item = filteredUnused.find((u: any) => (u.entity_id || u.name) === selectedDeadCodeItem);
                  if (!item) return null;
                  return (
                    <div className="mt-4 p-4 bg-[#080D1A] border border-white/10 rounded-lg flex flex-wrap items-center justify-between gap-4 text-xs">
                      <div>
                        <div className="font-mono font-bold text-indigo-400 text-sm">{item.entity_id || item.name}</div>
                        <div className="text-slate-400 font-mono text-[11px] mt-0.5">{item.file_path || item.name}</div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-center bg-white/5 border border-white/5 rounded-lg px-3 py-1.5">
                          <div className="text-[9px] font-bold text-slate-400 uppercase">RISK</div>
                          <div className="text-sm font-bold text-amber-400">{item.risk_level || 'HIGH'}</div>
                        </div>
                        <div className="text-center bg-white/5 border border-white/5 rounded-lg px-3 py-1.5">
                          <div className="text-[9px] font-bold text-slate-400 uppercase">CONFIDENCE</div>
                          <div className="text-sm font-bold text-white">{((item.unused_probability || 0) * 100).toFixed(1)}%</div>
                        </div>
                        <div className="text-center bg-white/5 border border-white/5 rounded-lg px-3 py-1.5">
                          <div className="text-[9px] font-bold text-slate-400 uppercase">REFERENCES</div>
                          <div className="text-sm font-bold text-white">{item.reference_count || 0}</div>
                        </div>
                      </div>
                    </div>
                  );
                })()}
              </div>

              {/* Dead Code Table Dropdown Expander */}
              <Expander title={`Dead Code Candidates Table (${filteredUnused.length} Candidates)`} defaultOpen={true}>
                <div className="border border-white/10 rounded-lg overflow-hidden bg-[#0A0E1A]">
                  <div className="max-h-[420px] overflow-y-auto overflow-x-auto">
                    <table className="w-full text-left border-collapse table-fixed min-w-[960px]">
                      <thead className="sticky top-0 z-10">
                        <tr className="bg-[#0E131F] border-b border-white/10 shadow-sm">
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 border-r border-white/10 w-[260px]">Component</th>
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 border-r border-white/10 w-[75px]">Type</th>
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 border-r border-white/10 w-[260px]">File</th>
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 border-r border-white/10 text-right w-[85px]">References</th>
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 border-r border-white/10 text-right w-[95px]">Confidence</th>
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 border-r border-white/10 w-[80px]">Risk Tier</th>
                          <th className="py-2.5 px-3 text-xs font-semibold text-slate-300 min-w-[180px]">Evidence</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-white/5">
                        {filteredUnused.map((u: any, i: number) => {
                          const compPath = u.entity_id || u.name;
                          const filePath = u.file_path || u.name;
                          const typeStr = String(u.type || 'file').toUpperCase();
                          const refCount = u.reference_count || 0;
                          const confidenceStr = `${((u.unused_probability || 0) * 100).toFixed(1)}%`;
                          const riskTier = u.risk_level || 'HIGH';
                          const evidence = (u.reasons && u.reasons[0]) || (refCount === 0 ? 'Zero static incoming references' : 'No incoming references');

                          return (
                            <tr key={i} className="hover:bg-white/[0.02] transition-colors">
                              <td className="py-2 px-3 text-xs font-mono text-slate-300 border-r border-white/5 truncate max-w-[260px]" title={compPath}>
                                {compPath}
                              </td>
                              <td className="py-2 px-3 text-xs text-slate-300 border-r border-white/5">
                                {typeStr}
                              </td>
                              <td className="py-2 px-3 text-xs font-mono text-slate-300 border-r border-white/5 truncate max-w-[260px]" title={filePath}>
                                {filePath}
                              </td>
                              <td className="py-2 px-3 text-xs font-mono text-slate-300 border-r border-white/5 text-right">
                                {refCount}
                              </td>
                              <td className="py-2 px-3 text-xs font-mono text-slate-300 border-r border-white/5 text-right">
                                {confidenceStr}
                              </td>
                              <td className="py-2 px-3 text-xs text-slate-300 border-r border-white/5 font-medium">
                                {riskTier}
                              </td>
                              <td className="py-2 px-3 text-xs text-slate-300 truncate" title={evidence}>
                                {evidence}
                              </td>
                            </tr>
                          );
                        })}
                        {filteredUnused.length === 0 && (
                          <tr>
                            <td colSpan={7} className="py-8 text-center text-xs text-slate-500">
                              No unused code candidates match the current filter.
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </Expander>

              {/* Expander: Groq AI Dead Code Advisory */}
              <Expander title={`Groq AI Dead Code Advisory & Pruning Protocol (${filteredUnused.length} Candidates)`} defaultOpen={false}>
                <p className="text-xs text-slate-400 mb-3">
                  Audit all {filteredUnused.length} components with Groq AI to classify framework entry points, active references, and safe-to-prune dead code.
                </p>
                {!aiUnused.content && !aiUnused.loading ? (
                  <button
                    onClick={handleAiUnused}
                    className="bg-[#1E2538] hover:bg-[#2A344D] text-white border border-white/10 text-xs px-4 py-2 rounded-lg font-medium transition-colors"
                  >
                    Evaluate Pruning Safety for Table Candidates ({filteredUnused.length} items)
                  </button>
                ) : aiUnused.loading ? (
                  <div className="text-xs text-indigo-400 animate-pulse py-2">
                    Evaluating pruning safety with Groq AI...
                  </div>
                ) : (
                  <div className="ai-response pt-2">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{aiUnused.content}</ReactMarkdown>
                    <button
                      onClick={handleAiUnused}
                      className="bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 text-xs px-3 py-1.5 rounded-md mt-4 transition-colors"
                    >
                      Re-evaluate Candidates
                    </button>
                  </div>
                )}
              </Expander>
            </div>
          );
        })()}

        {/* TAB 5: ML EXPLAINABILITY */}
        {activeTab === 'explainability' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-white tracking-tight mb-1">
                Machine Learning Model Calibration &amp; Explainability
              </h2>
              <p className="text-xs text-slate-400">
                Insights into feature attribution weights, ROC curve calibration, and decision matrices.
              </p>
            </div>

            {!modelsMeta ? (
              <div className="text-xs text-slate-400 animate-pulse p-4">Loading model metadata...</div>
            ) : (
              <>
                {/* Row 1: Feature Importance */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="glass-card p-6">
                    <h3 className="text-sm font-bold text-white mb-4">Impact Model Feature Importance</h3>
                    <FeatureImportanceBar importances={modelsMeta.impact_model?.feature_importance} title="" />
                  </div>
                  <div className="glass-card p-6">
                    <h3 className="text-sm font-bold text-white mb-4">Dead Code Feature Importance</h3>
                    <FeatureImportanceBar importances={modelsMeta.unused_model?.feature_importance} title="" />
                  </div>
                </div>

                {/* Row 2: Calibration & Confusion Matrix */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="glass-card p-6">
                    <h3 className="text-sm font-bold text-white mb-4">Model Calibration (ROC Curve)</h3>
                    <RocCurve
                      rocData={modelsMeta.impact_model?.roc_curve}
                      aucScore={modelsMeta.impact_model?.roc_auc}
                    />
                  </div>
                  <div className="glass-card p-6">
                    <h3 className="text-sm font-bold text-white mb-4">Decision Boundaries (Confusion Matrix)</h3>
                    <ConfusionMatrix cm={modelsMeta.impact_model?.confusion_matrix} />
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* TAB 6: AUDIT REPORTS */}
        {activeTab === 'reports' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-white tracking-tight mb-1">
                Architectural Audit Reports &amp; Export
              </h2>
              <p className="text-xs text-slate-400">
                Generate complete project audit documentation and download in structured formats.
              </p>
            </div>

            {/* 3 Full-Width Download Buttons in Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                onClick={() => handleExport('pdf')}
                disabled={exportingFormat !== null}
                className="bg-[#0D1220] hover:bg-[#161B28] border border-white/10 text-slate-200 py-3.5 px-4 rounded-xl text-xs font-semibold text-center transition-all shadow-sm"
              >
                {exportingFormat === 'pdf' ? 'Generating PDF...' : 'Download PDF Report'}
              </button>
              <button
                onClick={() => handleExport('docx')}
                disabled={exportingFormat !== null}
                className="bg-[#0D1220] hover:bg-[#161B28] border border-white/10 text-slate-200 py-3.5 px-4 rounded-xl text-xs font-semibold text-center transition-all shadow-sm"
              >
                {exportingFormat === 'docx' ? 'Generating Word...' : 'Download Word Report (.docx)'}
              </button>
              <button
                onClick={() => handleExport('csv')}
                disabled={exportingFormat !== null}
                className="bg-[#0D1220] hover:bg-[#161B28] border border-white/10 text-slate-200 py-3.5 px-4 rounded-xl text-xs font-semibold text-center transition-all shadow-sm"
              >
                {exportingFormat === 'csv' ? 'Generating CSV...' : 'Download CSV Report'}
              </button>
            </div>

            {/* Audit Report Preview */}
            <div>
              <h3 className="text-lg font-bold text-white mb-3">Audit Report Preview</h3>
              <div className="glass-card p-6">
                <div className="bg-[#080D1A] rounded-xl p-6 font-mono text-xs leading-loose overflow-x-auto border border-white/5">
                  <div className="text-cyan-400 mb-1 flex items-center gap-1.5 font-bold">
                    <span className="text-[10px]">▼</span>
                    <span>&#123;</span>
                  </div>
                  <div className="pl-6 space-y-1.5 text-slate-300">
                    <div>
                      <span className="text-amber-300">"project"</span> : <span className="text-emerald-400">"{projectName}"</span>
                    </div>
                    <div>
                      <span className="text-amber-300">"timestamp"</span> : <span className="text-emerald-400">"{scanInfo.timestamp || new Date().toISOString()}"</span>
                    </div>
                    <div>
                      <span className="text-amber-300">"total_files"</span> : <span className="text-cyan-300">{totalFiles}</span>
                    </div>
                    <div>
                      <span className="text-amber-300">"total_code_lines"</span> : <span className="text-cyan-300">{totalLoc}</span>
                    </div>
                    <div>
                      <span className="text-amber-300">"dependencies_count"</span> : <span className="text-cyan-300">{totalEdges}</span>
                    </div>
                    <div>
                      <span className="text-amber-300">"dead_code_candidates"</span> : <span className="text-cyan-300">{unusedResults.length}</span>
                    </div>
                    <div>
                      <span className="text-amber-300">"circular_dependencies"</span> : <span className="text-cyan-300">{cycles.length}</span>
                    </div>
                  </div>
                  <div className="text-cyan-400 mt-1 font-bold">&#125;</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
