export interface UploadResult {
  session_id: string;
  project_name: string;
  total_files: number;
  total_code_lines: number;
}

export interface SessionData {
  scan_info: Record<string, any>;
  metrics: Record<string, any>;
  top_hubs: any[];
  cycles: any[];
  has_cycles: boolean;
  unused_results: any[];
  graph_nodes: any[];
  graph_edges: any[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function uploadZip(file: File, projectName?: string): Promise<UploadResult> {
  const formData = new FormData();
  formData.append('file', file);
  if (projectName) formData.append('project_name', projectName);
  const res = await fetch(`${API_URL}/api/upload`, { method: 'POST', body: formData });
  if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Upload failed'); }
  return res.json();
}

export async function analyzeLocal(path: string, projectName?: string): Promise<UploadResult> {
  const res = await fetch(`${API_URL}/api/analyze/local`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, project_name: projectName || '' }),
  });
  if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Local analysis failed'); }
  return res.json();
}

export async function getSession(sessionId: string): Promise<SessionData> {
  const res = await fetch(`${API_URL}/api/session/${sessionId}`);
  if (!res.ok) throw new Error('Session fetch failed');
  return res.json();
}

export async function getImpact(
  sessionId: string,
  component: string,
  fallback?: { graph_nodes?: any[]; graph_edges?: any[] }
): Promise<any> {
  const res = await fetch(`${API_URL}/api/impact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      component,
      graph_nodes: fallback?.graph_nodes,
      graph_edges: fallback?.graph_edges,
    }),
  });
  if (!res.ok) {
    const err = await res.text().catch(() => '');
    throw new Error(`Impact API error (${res.status}): ${err || 'Failed to fetch impact data'}`);
  }
  return res.json();
}

export async function getAiArch(sessionId: string): Promise<{ content: string }> {
  const res = await fetch(`${API_URL}/api/ai/arch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  });
  if (!res.ok) throw new Error('Failed to fetch AI architecture assessment');
  return res.json();
}

export async function getAiImpact(sessionId: string, component: string, impactRes: any): Promise<{ content: string }> {
  const res = await fetch(`${API_URL}/api/ai/impact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, component, impact_res: impactRes }),
  });
  if (!res.ok) throw new Error('Failed to fetch AI impact analysis');
  return res.json();
}

export async function getAiUnused(sessionId: string, unusedCandidates: any[], filterContext?: any): Promise<{ content: string }> {
  const res = await fetch(`${API_URL}/api/ai/unused`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, unused_candidates: unusedCandidates, filter_context: filterContext }),
  });
  if (!res.ok) throw new Error('Failed to fetch AI dead code advisory');
  return res.json();
}

export async function getModelsMeta(): Promise<any> {
  const res = await fetch(`${API_URL}/api/models/meta`);
  if (!res.ok) throw new Error('Failed to fetch models metadata');
  return res.json();
}

export async function exportReport(
  sessionId: string,
  format: 'pdf' | 'docx' | 'csv' | 'html' | 'json',
  fallbackData?: Record<string, any>
): Promise<Blob> {
  const payload: Record<string, any> = {
    session_id: sessionId,
    format,
    ...(fallbackData || {})
  };
  const res = await fetch(`${API_URL}/api/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to export report' }));
    throw new Error(err.detail || 'Failed to export report');
  }
  return res.blob();
}
