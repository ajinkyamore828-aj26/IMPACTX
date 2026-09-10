import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from backend.session_store import store

router = APIRouter()

class AIArchRequest(BaseModel):
    session_id: str

class AIImpactRequest(BaseModel):
    session_id: str
    component: str
    impact_res: Dict[str, Any]

class AIUnusedRequest(BaseModel):
    session_id: str
    unused_candidates: List[Any]
    filter_context: Optional[Dict[str, Any]] = None

@router.post("/arch")
async def explain_architecture(req: AIArchRequest):
    session_data = store.get(req.session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        from src.llm.gemini_engine import GeminiEngine
        engine = GeminiEngine()
        
        scan_info = session_data.get("scan_info", {})
        metrics = session_data.get("metrics", {})
        top_hubs = session_data.get("top_hubs", [])
        cycles = session_data.get("cycles", [])
        
        result_str = engine.generate_architecture_summary(scan_info, metrics, top_hubs, cycles)
        return {"content": result_str}
    except ImportError:
        raise HTTPException(status_code=503, detail={"content": None})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/impact")
async def explain_impact(req: AIImpactRequest):
    session_data = store.get(req.session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        from src.llm.gemini_engine import GeminiEngine
        engine = GeminiEngine()
        
        result_str = engine.explain_impact(req.component, req.impact_res)
        return {"content": result_str}
    except ImportError:
        raise HTTPException(status_code=503, detail={"content": None})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/unused")
async def explain_unused(req: AIUnusedRequest):
    session_data = store.get(req.session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        from src.llm.gemini_engine import GeminiEngine
        engine = GeminiEngine()
        
        result_str = engine.explain_unused_code(req.unused_candidates, filter_context=req.filter_context)
        return {"content": result_str}
    except ImportError:
        raise HTTPException(status_code=503, detail={"content": None})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
