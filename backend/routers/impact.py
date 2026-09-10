import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # repo root

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import networkx as nx
from session_store import store
import json

router = APIRouter()

from typing import Optional, List, Dict, Any

class ImpactRequest(BaseModel):
    session_id: str
    component: str
    graph_nodes: Optional[List[Dict[str, Any]]] = None
    graph_edges: Optional[List[Dict[str, Any]]] = None

@router.post("/impact")
async def analyze_impact(req: ImpactRequest):
    session_data = store.get(req.session_id) or {}
    if req.graph_nodes is not None:
        session_data.setdefault("graph_nodes", req.graph_nodes)
    if req.graph_edges is not None:
        session_data.setdefault("graph_edges", req.graph_edges)
    if not session_data.get("graph_nodes"):
        raise HTTPException(status_code=404, detail="Session not found")
    store.set(req.session_id, session_data)


    try:
        from src.graph.dependency_graph import DependencyGraph
        from src.analysis.impact_analyzer import ImpactAnalyzer

        G = nx.DiGraph()
        nodes = session_data.get("graph_nodes", [])
        edges = session_data.get("graph_edges", [])

        for n in nodes:
            node_data = dict(n)  # copy to avoid mutating stored session
            node_id = node_data.pop("id")
            G.add_node(node_id, **node_data)

        for e in edges:
            edge_data = dict(e)  # copy to avoid mutating stored session
            u = edge_data.pop("source")
            v = edge_data.pop("target")
            G.add_edge(u, v, **edge_data)

        dep_graph_obj = DependencyGraph()
        dep_graph_obj.graph = G

        analyzer = ImpactAnalyzer(dep_graph_obj)
        impact_res = analyzer.analyze_impact(req.component)

        impact_res = json.loads(json.dumps(impact_res, default=lambda o: float(o) if hasattr(o, '__float__') else str(o)))

        return impact_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

