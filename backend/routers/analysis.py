import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # repo root

import os
import tempfile
import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from session_store import store
from pydantic import BaseModel
import networkx as nx

router = APIRouter()

class LocalAnalyzeRequest(BaseModel):
    path: str
    project_name: str = ""

def run_project_analysis(target_dir, project_name=""):
    from src.analysis.project_scanner import ProjectScanner
    from src.analysis.dependency_analyzer import DependencyAnalyzer
    from src.analysis.unused_code_analyzer import UnusedCodeAnalyzer
    from src.graph.graph_metrics import GraphMetricsEngine
    from src.graph.cycle_detector import CycleDetector
    
    scanner = ProjectScanner(target_dir)
    scan_info = scanner.scan()
    if project_name:
        scan_info["project_name"] = project_name
    
    dep_analyzer = DependencyAnalyzer(target_dir)
    dep_graph = dep_analyzer.analyze(scan_info["files"])
    
    metrics = GraphMetricsEngine.compute_all_metrics(dep_graph)
    top_hubs = GraphMetricsEngine.get_top_hubs(dep_graph, top_n=20)
    cycles = CycleDetector.find_cycles(dep_graph)
    has_cycles = len(cycles) > 0
    
    unused_analyzer = UnusedCodeAnalyzer(dep_graph)
    unused_results = unused_analyzer.analyze_unused()
    
    # Serialize graph for JSON storage
    graph_nodes = []
    for node in dep_graph.graph.nodes(data=True):
        graph_nodes.append({"id": node[0], **node[1]})
    graph_edges = [{"source": u, "target": v, **d} for u, v, d in dep_graph.graph.edges(data=True)]
    
    clean_metrics = json.loads(json.dumps(metrics, default=lambda o: float(o) if hasattr(o, '__float__') else str(o)))
    
    return {
        "scan_info": scan_info,
        "metrics": clean_metrics,
        "top_hubs": top_hubs,
        "cycles": cycles,
        "has_cycles": has_cycles,
        "unused_results": unused_results,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
    }

@router.post("/upload")
async def upload_project(file: UploadFile = File(...), project_name: str = Form("")):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")
    
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(zip_path, "wb") as f:
            f.write(await file.read())
        
        from src.utils.zip_handler import safe_extract_zip
        extracted_path = safe_extract_zip(zip_path)
        
        result_dict = run_project_analysis(extracted_path, project_name)
        sid = store.create(result_dict)
        
        scan_info = result_dict.get("scan_info", {})
        return {
            "session_id": sid,
            "project_name": scan_info.get("project_name", project_name),
            "total_files": scan_info.get("total_files", 0),
            "total_code_lines": scan_info.get("total_lines", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze/local")
async def analyze_local(req: LocalAnalyzeRequest):
    if not os.path.exists(req.path):
        raise HTTPException(status_code=400, detail="Path does not exist")
    
    target_dir = req.path
    if req.path.endswith(".zip"):
        from src.utils.zip_handler import safe_extract_zip
        try:
            target_dir = safe_extract_zip(req.path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract zip: {str(e)}")
            
    try:
        result_dict = run_project_analysis(target_dir, req.project_name)
        sid = store.create(result_dict)
        
        scan_info = result_dict.get("scan_info", {})
        return {
            "session_id": sid,
            "project_name": scan_info.get("project_name", req.project_name),
            "total_files": scan_info.get("total_files", 0),
            "total_code_lines": scan_info.get("total_lines", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Retrieve full analysis session data by session ID."""
    session_data = store.get(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return session_data
