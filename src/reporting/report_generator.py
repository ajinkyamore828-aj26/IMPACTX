"""
Report generator for impactx.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from src.reporting.export_formats import (
    export_to_json,
    export_to_csv,
    export_to_html,
    export_to_pdf,
    export_to_docx,
)
from src.utils.logger import get_logger

logger = get_logger("report_generator")

class ReportGenerator:
    """Generates structured project audits and handles exports."""

    @classmethod
    def compile_report(
        cls,
        scan_data: Dict[str, Any],
        graph_data: Dict[str, Any],
        unused_candidates: List[Dict[str, Any]],
        top_hubs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Assembles a full audit report dictionary with risk distribution and health metrics."""
        crit_count = sum(1 for u in unused_candidates if str(u.get("risk_level", "")).upper() == "CRITICAL")
        high_count = sum(1 for u in unused_candidates if str(u.get("risk_level", "")).upper() == "HIGH")
        med_count = sum(1 for u in unused_candidates if str(u.get("risk_level", "")).upper() == "MEDIUM")
        low_count = sum(1 for u in unused_candidates if str(u.get("risk_level", "")).upper() == "LOW")

        has_cycles = bool(graph_data.get("has_cycles", False))
        cycles = graph_data.get("cycles", [])
        cycles_count = len(cycles)

        # Architectural health score (0-100)
        penalty = 0
        if has_cycles:
            penalty += 25 + min(15, cycles_count * 5)
        penalty += min(25, crit_count * 4)
        penalty += min(15, high_count * 2)
        health_score = max(15, 100 - penalty)

        return {
            "title": "impactx Architectural Audit",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "iso_timestamp": datetime.now().isoformat(),
            "project_name": scan_data.get("project_name", "Unknown"),
            "health_score": health_score,
            "total_files": scan_data.get("total_files", 0),
            "total_lines": scan_data.get("total_lines", 0),
            "total_code_lines": scan_data.get("total_code_lines", 0),
            "language_distribution": scan_data.get("language_distribution", {}),
            "total_nodes": graph_data.get("total_nodes", 0),
            "total_dependencies": graph_data.get("total_edges", 0),
            "has_cycles": has_cycles,
            "cycles_count": cycles_count,
            "cycles": cycles,
            "top_hubs": top_hubs,
            "unused_candidates": unused_candidates,
            "critical_risk_unused_count": crit_count,
            "high_risk_unused_count": high_count,
            "medium_risk_unused_count": med_count,
            "low_risk_unused_count": low_count,
            "risk_breakdown": {
                "CRITICAL": crit_count,
                "HIGH": high_count,
                "MEDIUM": med_count,
                "LOW": low_count,
            },
        }

    @classmethod
    def export(cls, report_data: Dict[str, Any], format_type: str, output_path: Optional[Path] = None, theme: str = "dark") -> Any:
        """Exports report in requested format: pdf, docx, csv, json, or html."""
        format_lower = str(format_type).lower().strip()
        if format_lower == "pdf":
            return export_to_pdf(report_data, output_path)
        elif format_lower in ("docx", "word"):
            return export_to_docx(report_data, output_path)
        elif format_lower == "csv":
            return export_to_csv(report_data, output_path)
        elif format_lower == "json":
            return export_to_json(report_data, output_path)
        elif format_lower in ("html", "htm"):
            return export_to_html(report_data, output_path, theme=theme)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
