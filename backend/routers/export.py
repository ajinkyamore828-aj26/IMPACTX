import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # repo root

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from session_store import store

router = APIRouter()

class ExportRequest(BaseModel):
    session_id: str
    format: str
    scan_info: Optional[Dict[str, Any]] = None
    top_hubs: Optional[List[Dict[str, Any]]] = None
    unused_results: Optional[List[Dict[str, Any]]] = None
    graph_nodes: Optional[List[Dict[str, Any]]] = None
    graph_edges: Optional[List[Dict[str, Any]]] = None
    has_cycles: Optional[bool] = False
    cycles: Optional[List[Any]] = None
    theme: Optional[str] = "dark"

@router.get("/models/meta")
async def get_models_meta():
    try:
        from src.ml.model_loader import ModelRegistry
        return ModelRegistry.get_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
async def export_report(req: ExportRequest):
    format_type = req.format.lower().strip()
    valid_formats = ["pdf", "docx", "word", "csv", "html", "htm", "json"]
    if format_type not in valid_formats:
        raise HTTPException(status_code=400, detail=f"Invalid format: {req.format}. Supported: {valid_formats}")

    session_data = store.get(req.session_id) or {}
    
    # 1. Merge scan_info (prefer client if non-empty, else session_data)
    req_scan = req.scan_info or {}
    store_scan = session_data.get("scan_info") or {}
    scan_info = dict(store_scan)
    scan_info.update({k: v for k, v in req_scan.items() if v is not None and v != "" and v != 0})

    # 2. Merge top_hubs
    top_hubs = req.top_hubs if (req.top_hubs and len(req.top_hubs) > 0) else session_data.get("top_hubs", [])

    # 3. Merge unused_results
    unused_results = req.unused_results if (req.unused_results and len(req.unused_results) > 0) else session_data.get("unused_results", [])

    # 4. Merge graph_nodes and graph_edges
    graph_nodes = req.graph_nodes if (req.graph_nodes and len(req.graph_nodes) > 0) else session_data.get("graph_nodes", [])
    graph_edges = req.graph_edges if (req.graph_edges and len(req.graph_edges) > 0) else session_data.get("graph_edges", [])

    # 5. Merge cycles
    has_cycles = req.has_cycles if req.has_cycles is not None else session_data.get("has_cycles", False)
    cycles = req.cycles if (req.cycles and len(req.cycles) > 0) else session_data.get("cycles", [])

    # 6. Intelligent Hydration from Graph Entities if scan_info or tables are empty
    if (not scan_info.get("total_files") or not scan_info.get("project_name") or scan_info.get("project_name") == "Unknown") and graph_nodes:
        file_nodes = [n for n in graph_nodes if n.get("type") == "file"]
        if file_nodes:
            scan_info["total_files"] = len(file_nodes)
            scan_info["total_code_lines"] = sum(n.get("code_lines") or n.get("lines_of_code") or 0 for n in file_nodes)
            lang_dist = {}
            for n in file_nodes:
                l = n.get("language") or "Unknown"
                if l != "Unknown":
                    lang_dist[l] = lang_dist.get(l, 0) + 1
            scan_info["language_distribution"] = lang_dist
            sample_path = file_nodes[0].get("file_path") or file_nodes[0].get("id", "")
            if sample_path:
                parts = sample_path.replace("\\", "/").split("/")
                scan_info["project_name"] = parts[0] if parts else "project"
        else:
            scan_info["total_files"] = len(graph_nodes)
            scan_info["total_code_lines"] = sum(n.get("code_lines") or n.get("lines_of_code") or 0 for n in graph_nodes)

    # 7. Hydrate top_hubs using NetworkX if empty
    if not top_hubs and graph_nodes and graph_edges:
        import networkx as nx
        G = nx.DiGraph()
        for n in graph_nodes:
            nd = dict(n)
            nid = nd.pop("id", "")
            if nid:
                G.add_node(nid, **nd)
        for e in graph_edges:
            ed = dict(e)
            u = ed.pop("source", "")
            v = ed.pop("target", "")
            if u and v:
                G.add_edge(u, v, **ed)
        
        try:
            pr = nx.pagerank(G, alpha=0.85, max_iter=100)
        except Exception:
            pr = {node: 1.0 / (len(G) or 1) for node in G.nodes()}
            
        hub_list = []
        for node in G.nodes():
            node_data = G.nodes[node]
            in_d = G.in_degree(node)
            out_d = G.out_degree(node)
            hub_list.append({
                "id": node,
                "entity_type": node_data.get("type", "file"),
                "pagerank": float(pr.get(node, 0.0)),
                "in_degree": int(in_d),
                "out_degree": int(out_d),
            })
        hub_list.sort(key=lambda x: (x["in_degree"], x["pagerank"]), reverse=True)
        top_hubs = hub_list[:30]

    # 8. Hydrate unused_results if empty
    if not unused_results and graph_nodes and graph_edges:
        if 'G' not in locals():
            import networkx as nx
            G = nx.DiGraph()
            for n in graph_nodes:
                nd = dict(n)
                nid = nd.pop("id", "")
                if nid:
                    G.add_node(nid, **nd)
            for e in graph_edges:
                ed = dict(e)
                u = ed.pop("source", "")
                v = ed.pop("target", "")
                if u and v:
                    G.add_edge(u, v, **ed)
        
        reconstructed_unused = []
        for node in G.nodes():
            in_d = G.in_degree(node)
            if in_d == 0:
                node_data = G.nodes[node]
                entity_type = node_data.get("type", "file")
                name = node_data.get("name") or node.split("/")[-1]
                file_p = node_data.get("file_path") or node
                reconstructed_unused.append({
                    "entity_id": node,
                    "name": name,
                    "type": entity_type,
                    "file_path": file_p,
                    "reference_count": 0,
                    "unused_probability": 0.95,
                    "risk_level": "HIGH" if entity_type == "file" else "MEDIUM",
                    "reasons": ["Zero incoming static references detected"],
                })
        unused_results = reconstructed_unused[:60]

    # 9. Update store with complete hydrated dictionary
    full_session_data = {
        "scan_info": scan_info,
        "top_hubs": top_hubs,
        "unused_results": unused_results,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
        "has_cycles": has_cycles,
        "cycles": cycles,
    }
    store.set(req.session_id, full_session_data)

    try:
        from src.reporting.report_generator import ReportGenerator
        
        graph_data = {
            "total_nodes": len(graph_nodes),
            "total_edges": len(graph_edges),
            "has_cycles": has_cycles,
            "cycles": cycles
        }
        
        report_data = ReportGenerator.compile_report(
            scan_data=scan_info, 
            graph_data=graph_data, 
            unused_candidates=unused_results, 
            top_hubs=top_hubs
        )
        
        raw_output = ReportGenerator.export(report_data, format_type, theme=req.theme or "dark")
        
        if isinstance(raw_output, str):
            bytes_data = raw_output.encode("utf-8")
        else:
            bytes_data = raw_output
            
        proj_name = scan_info.get("project_name", "project").replace(" ", "_")
        
        if format_type == "pdf":
            media_type = "application/pdf"
            filename = f"impactx_audit_report_{proj_name}.pdf"
        elif format_type in ("docx", "word"):
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"impactx_audit_report_{proj_name}.docx"
        elif format_type == "csv":
            media_type = "text/csv; charset=utf-8"
            filename = f"impactx_audit_report_{proj_name}.csv"
        elif format_type in ("html", "htm"):
            media_type = "text/html; charset=utf-8"
            filename = f"impactx_audit_report_{proj_name}.html"
        elif format_type == "json":
            media_type = "application/json"
            filename = f"impactx_audit_report_{proj_name}.json"
            
        return Response(
            content=bytes_data, 
            media_type=media_type, 
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
