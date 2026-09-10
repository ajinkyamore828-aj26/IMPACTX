"""
Enhanced Table components, styling, and data formatting for impactx dashboard.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd

def parse_entity_label(entity_id: str, default_type: str = "unknown") -> Tuple[str, str, str]:
    """
    Parses an entity ID into (display_name, file_path, short_location).
    Example:
      'task2/client/src/context/CartContext.jsx/useCart' ->
      display_name: 'useCart'
      file_path: 'task2/client/src/context/CartContext.jsx'
      short_location: 'src/context/CartContext.jsx'
    """
    parts = str(entity_id).replace("\\", "/").split("/")
    last_part = parts[-1]
    has_file_extension = any(last_part.endswith(ext) for ext in (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".html", ".css"))

    if has_file_extension:
        display_name = last_part
        file_path = "/".join(parts)
        short_location = "/".join(parts[-3:]) if len(parts) >= 3 else file_path
    else:
        display_name = last_part
        file_path = "/".join(parts[:-1]) if len(parts) > 1 else entity_id
        short_location = "/".join(parts[-3:]) if len(parts) >= 3 else file_path

    return display_name, file_path, short_location

def format_hubs_table(hubs_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """Formats list of high-impact hubs into an aligned, readable DataFrame."""
    rows = []
    for h in hubs_list:
        entity_id = h.get("id", "")
        display_name, file_path, _ = parse_entity_label(entity_id, h.get("entity_type", ""))
        
        rows.append({
            "Component": display_name,
            "Type": str(h.get("entity_type", "unknown")).upper(),
            "PageRank": float(h.get("pagerank", 0.0)),
            "Dependents (In)": int(h.get("in_degree", 0)),
            "Dependencies (Out)": int(h.get("out_degree", 0)),
            "File Location": file_path,
        })
    return pd.DataFrame(rows)

def format_impact_table(affected_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """Formats list of affected components into a clean DataFrame with numerical metrics."""
    rows = []
    for a in affected_list:
        component_id = a.get("component", "")
        display_name, file_path, _ = parse_entity_label(component_id, a.get("type", ""))

        rows.append({
            "Component": display_name,
            "Type": str(a.get("type", "unknown")).upper(),
            "Impact Level": a.get("level", "Direct"),
            "Hops": int(a.get("distance", 1)),
            "Impact Probability": float(a.get("probability", 0.0)),
            "Risk Tier": a.get("risk_level", "LOW"),
            "Key Driver": (a.get("explanations") or ["Static dependency path"])[0],
            "File Location": file_path,
        })
    return pd.DataFrame(rows)

def format_unused_table(unused_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """Formats list of unused code candidates into a clean DataFrame with numerical metrics."""
    rows = []
    for u in unused_list:
        name = u.get("name", "")
        file_path = u.get("file_path", "")
        
        rows.append({
            "Dead Component": name,
            "Type": str(u.get("type", "unknown")).upper(),
            "File Location": file_path,
            "References": int(u.get("reference_count", 0)),
            "Non-Use Probability": float(u.get("unused_probability", 0.0)),
            "Risk Tier": u.get("risk_level", "LOW"),
            "Evidence": (u.get("reasons") or ["Zero static incoming references"])[0],
        })
    return pd.DataFrame(rows)
