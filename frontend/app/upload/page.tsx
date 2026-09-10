'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import { uploadZip, analyzeLocal, getSession } from '@/lib/api';
import { saveSession } from '@/lib/store';
import {
  ArrowLeft,
  ArrowRight,
  FolderArchive,
  Folder,
  Upload,
  FileArchive,
  Check,
  X,
  ShieldCheck,
  Code2,
  Cpu,
  AlertCircle,
  Loader2,
} from 'lucide-react';

const STAGE_LABELS: Record<number, string> = {
  1: '1/4 Initializing local sandbox extraction...',
  2: '2/4 Parsing multi-language ASTs (Python, JS, TS, HTML, CSS)...',
  3: '3/4 Modeling NetworkX dependency graph & calculating PageRank...',
  4: '4/4 Running ML blast radius & dead code inference models...',
};

export default function UploadPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [mode, setMode] = useState<'zip' | 'dir'>('zip');
  const [file, setFile] = useState<File | null>(null);
  const [localPath, setLocalPath] = useState('');
  const [projectName, setProjectName] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);
  const [prevView, setPrevView] = useState('steps');

  useEffect(() => {
    setPrevView(localStorage.getItem('prevView') || 'steps');
  }, []);

  const handleFileSelect = (selectedFile: File | null) => {
    if (!selectedFile) return;
    if (!selectedFile.name.toLowerCase().endsWith('.zip')) {
      setError('Only .zip repository archives are supported.');
      return;
    }
    setError('');
    setFile(selectedFile);
    if (!projectName) {
      const cleanName = selectedFile.name.replace(/\.zip$/i, '');
      setProjectName(cleanName);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (mode === 'zip' && !file) {
      setError('Please select a ZIP file');
      return;
    }
    if (mode === 'dir' && !localPath.trim()) {
      setError('Please enter a valid local directory path');
      return;
    }

    setError('');
    setLoading(true);

    try {
      setProgress(1);
      let uploadRes;
      if (mode === 'zip') {
        uploadRes = await uploadZip(file!, projectName || undefined);
      } else {
        uploadRes = await analyzeLocal(localPath.trim(), projectName || undefined);
      }

      setProgress(2);
      await new Promise(r => setTimeout(r, 400));
      setProgress(3);
      await new Promise(r => setTimeout(r, 400));
      setProgress(4);

      const sessionData = await getSession(uploadRes.session_id);
      saveSession(uploadRes.session_id, sessionData);

      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'An error occurred during analysis');
      setLoading(false);
      setProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-[#080D1A] text-white flex flex-col">
      <Navbar currentView="projects" />

      {/* Back Button Aligned Directly Under 'impactx ML PLATFORM' */}
      <div className="max-w-7xl mx-auto w-full px-8 pt-4 pb-2">
        <button
          onClick={() => router.push(prevView === 'about' ? '/' : '/steps')}
          className="inline-flex items-center gap-2 bg-[#0E131F] hover:bg-[#161B28] text-slate-300 border border-white/10 rounded-lg px-4 py-2 text-xs font-semibold transition-all shadow-sm"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to {prevView === 'about' ? 'About' : 'Steps'}</span>
        </button>
      </div>

      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-4 flex flex-col justify-center">
        {/* Main Clean Ingestion Card */}
        <div className="bg-[#0E131F] border border-white/[0.08] rounded-xl max-w-2xl mx-auto w-full p-8 mb-8 text-center shadow-md">
          {/* Logo Node Icon Container */}
          <div className="w-11 h-11 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center mx-auto mb-3">
            <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <line x1="7" y1="7" x2="25" y2="25" stroke="#818CF8" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="25" y1="7" x2="7" y2="25" stroke="#818CF8" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="7" y1="16" x2="25" y2="16" stroke="#4F46E5" strokeWidth="1.5" strokeDasharray="2 2" strokeLinecap="round" />
              <circle cx="7" cy="7" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
              <circle cx="25" cy="7" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
              <circle cx="7" cy="25" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
              <circle cx="25" cy="25" r="3" fill="#312E81" stroke="#A5B4FC" strokeWidth="1.8" />
              <circle cx="16" cy="16" r="4.5" fill="#1E1B4B" stroke="#6366F1" strokeWidth="2" />
              <circle cx="16" cy="16" r="2" fill="#818CF8" />
            </svg>
          </div>

          <h1 className="text-xl font-bold text-white mb-2 tracking-tight">
            Upload Codebase Archive
          </h1>
          <p className="text-xs text-slate-400 max-w-lg mx-auto leading-relaxed mb-6">
            Upload a <code className="px-1.5 py-0.5 rounded bg-white/[0.06] text-slate-200 font-mono text-[11px] border border-white/10">.zip</code> repository archive or specify a local directory path to begin offline AST parsing &amp; ML blast radius prediction.
          </p>

          {/* Clean Segmented Ingestion Switcher */}
          <div className="bg-[#080D1A] border border-white/10 rounded-lg p-1 flex gap-1 mb-6 max-w-md mx-auto">
            <button
              type="button"
              onClick={() => { setMode('zip'); setError(''); }}
              className={`flex-1 py-2 px-3 text-xs font-semibold rounded-md transition-all flex items-center justify-center gap-1.5 ${
                mode === 'zip'
                  ? 'bg-[#4F46E5] text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <FolderArchive className="w-3.5 h-3.5" />
              <span>Upload Archive (.ZIP)</span>
            </button>
            <button
              type="button"
              onClick={() => { setMode('dir'); setError(''); }}
              className={`flex-1 py-2 px-3 text-xs font-semibold rounded-md transition-all flex items-center justify-center gap-1.5 ${
                mode === 'dir'
                  ? 'bg-[#4F46E5] text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Folder className="w-3.5 h-3.5" />
              <span>Direct Local Directory</span>
            </button>
          </div>

          {/* Input Area */}
          {mode === 'zip' ? (
            <div className="mb-5">
              {!file ? (
                /* Unselected State: Clean File Dropzone */
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`border border-dashed rounded-xl p-8 transition-colors cursor-pointer flex flex-col items-center justify-center ${
                    isDragging
                      ? 'border-indigo-500 bg-indigo-500/5'
                      : 'border-white/15 bg-[#080D1A] hover:border-white/25'
                  }`}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".zip"
                    onChange={e => handleFileSelect(e.target.files?.[0] || null)}
                    className="hidden"
                  />

                  <div className="bg-[#1C2333] hover:bg-[#252E44] border border-white/10 text-slate-200 text-xs font-semibold px-4 py-2 rounded-lg flex items-center gap-2 mb-2 transition-colors">
                    <Upload className="w-3.5 h-3.5" />
                    <span>Browse files</span>
                  </div>

                  <p className="text-xs text-slate-300 font-medium mb-1">
                    or drag and drop your .zip file here
                  </p>
                  <p className="text-[11px] text-slate-500">
                    Maximum upload limit: 1GB &bull; Processed 100% offline
                  </p>
                </div>
              ) : (
                /* Selected File Card: Clean, Monochromatic Enterprise State */
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4 text-left mb-5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5 text-emerald-400 font-semibold text-xs min-w-0">
                      <Check className="w-4 h-4 flex-shrink-0 text-emerald-400" />
                      <span className="truncate">
                        Archive Ready: <strong className="text-white">{file.name}</strong> ({(file.size / (1024 * 1024)).toFixed(1)} MB)
                      </span>
                    </div>

                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className="text-[10px] text-emerald-300 bg-emerald-500/20 px-2.5 py-0.5 rounded font-bold uppercase tracking-wider">
                        READY
                      </span>
                      <button
                        type="button"
                        onClick={() => {
                          setFile(null);
                          if (fileInputRef.current) fileInputRef.current.value = '';
                        }}
                        className="text-xs text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 border border-white/10 p-1 rounded transition-colors"
                        title="Remove file"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            /* Local Directory Ingestion Mode */
            <div className="border border-white/10 rounded-xl p-5 bg-[#080D1A] mb-5 text-left">
              <label className="block text-[11px] font-mono text-slate-400 uppercase tracking-wider mb-2">
                Absolute Local Directory or .ZIP Path
              </label>
              <input
                type="text"
                value={localPath}
                onChange={e => setLocalPath(e.target.value)}
                placeholder="e.g. C:\Users\eZee\projects\my-repo"
                className="w-full bg-[#0E131F] border border-white/10 rounded-lg px-4 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-colors font-mono mb-3"
              />

              <div className="flex items-center gap-3 pt-1">
                <label className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex-shrink-0">
                  Project Name (Optional):
                </label>
                <input
                  type="text"
                  value={projectName}
                  onChange={e => setProjectName(e.target.value)}
                  placeholder="e.g. my-repo"
                  className="flex-1 bg-[#0E131F] border border-white/10 rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-colors font-mono"
                />
              </div>
            </div>
          )}

          {/* Clean, Monochromatic Neutral Format Pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
            <span className="bg-white/[0.04] text-slate-400 px-3 py-1 rounded-md text-[11px] font-semibold border border-white/[0.08]">
              Python (.py)
            </span>
            <span className="bg-white/[0.04] text-slate-400 px-3 py-1 rounded-md text-[11px] font-semibold border border-white/[0.08]">
              JavaScript (.js, .jsx)
            </span>
            <span className="bg-white/[0.04] text-slate-400 px-3 py-1 rounded-md text-[11px] font-semibold border border-white/[0.08]">
              TypeScript (.ts, .tsx)
            </span>
            <span className="bg-white/[0.04] text-slate-400 px-3 py-1 rounded-md text-[11px] font-semibold border border-white/[0.08]">
              HTML5 (.html)
            </span>
            <span className="bg-white/[0.04] text-slate-400 px-3 py-1 rounded-md text-[11px] font-semibold border border-white/[0.08]">
              CSS3 (.css)
            </span>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs p-3 rounded-lg mb-4 text-center flex items-center justify-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Progress / Action Button */}
          {loading ? (
            <div className="space-y-2 py-2">
              <div className="flex justify-between text-xs text-slate-400">
                <span className="flex items-center gap-2">
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-400" />
                  {STAGE_LABELS[progress] || 'Analyzing codebase...'}
                </span>
                <span>{progress * 25}%</span>
              </div>
              <div className="progress-bar w-full bg-slate-800">
                <div className="progress-fill" style={{ width: `${progress * 25}%` }}></div>
              </div>
            </div>
          ) : (
            <button
              onClick={handleUpload}
              disabled={mode === 'zip' ? !file : !localPath.trim()}
              className={`w-full py-3 px-4 rounded-lg text-xs font-semibold transition-all flex items-center justify-center gap-2 ${
                (mode === 'zip' ? !!file : !!localPath.trim())
                  ? 'bg-[#4F46E5] hover:bg-[#4338CA] text-white shadow-sm cursor-pointer'
                  : 'bg-white/5 text-slate-500 border border-white/5 cursor-not-allowed'
              }`}
            >
              <span>
                {mode === 'zip'
                  ? (file ? `Extract & Run Full Analysis on ${file.name}` : 'Select a ZIP Archive to Analyze')
                  : (localPath.trim() ? 'Scan & Ingest Local Path' : 'Enter a Directory Path to Analyze')}
              </span>
              {(mode === 'zip' ? !!file : !!localPath.trim()) && <ArrowRight className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>

        {/* 3 Bottom Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 max-w-2xl mx-auto w-full">
          {/* Card 1 */}
          <div className="glass-card p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center mb-2">
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center mr-2 text-indigo-400">
                  <ShieldCheck className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-xs font-bold text-white">1. Sandboxed Extraction</h3>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed mb-4">
                Archives are strictly validated with Zip-Slip traversal protection and extracted into an isolated local sandbox.
              </p>
            </div>
            <div>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2 py-0.5 rounded-md inline-block">
                Zip-Slip Protection
              </span>
            </div>
          </div>

          {/* Card 2 */}
          <div className="glass-card p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center mb-2">
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center mr-2 text-indigo-400">
                  <Code2 className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-xs font-bold text-white">2. Multi-Language AST</h3>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed mb-4">
                Parsers scan files to catalog imports, exports, functions, and classes across polyglot repositories without running code.
              </p>
            </div>
            <div>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2 py-0.5 rounded-md inline-block">
                AST Tokenizer
              </span>
            </div>
          </div>

          {/* Card 3 */}
          <div className="glass-card p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center mb-2">
                <div className="w-7 h-7 rounded-lg bg-white/[0.04] border border-white/10 flex items-center justify-center mr-2 text-indigo-400">
                  <Cpu className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-xs font-bold text-white">3. ML Topology Inference</h3>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed mb-4">
                Compiles NetworkX graph models to compute PageRank centrality, predict XGBoost blast radius, and detect dead code.
              </p>
            </div>
            <div>
              <span className="text-[10px] font-mono text-slate-400 bg-white/5 border border-white/10 px-2 py-0.5 rounded-md inline-block">
                XGBoost &amp; Random Forest
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
