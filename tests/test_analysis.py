"""
End-to-end integration tests for impactx.
"""

from pathlib import Path
from config.config import SAMPLES_DIR
from src.utils.zip_handler import safe_extract_zip
from src.analysis.project_scanner import ProjectScanner
from src.analysis.dependency_analyzer import DependencyAnalyzer
from src.analysis.impact_analyzer import ImpactAnalyzer
from src.analysis.unused_code_analyzer import UnusedCodeAnalyzer
from src.reporting.report_generator import ReportGenerator

def test_full_analysis_pipeline():
    sample_zip = SAMPLES_DIR / "python_demo.zip"
    assert sample_zip.exists()

    extracted = safe_extract_zip(sample_zip)
    
    # 1. Scan
    scanner = ProjectScanner(extracted)
    scan_info = scanner.scan()
    assert scan_info["total_files"] >= 5
    assert "Python" in scan_info["language_distribution"]

    # 2. Dependency Graph
    dep_analyzer = DependencyAnalyzer(extracted)
    graph = dep_analyzer.analyze(scan_info["files"])
    assert graph.number_of_nodes > 0
    assert graph.number_of_edges > 0

    # 3. Impact Analysis
    impact_engine = ImpactAnalyzer(graph)
    # Check impact of database.py
    impact_res = impact_engine.analyze_impact("database.py")
    assert impact_res["total_affected"] > 0

    # 4. Unused Code Analysis
    unused_engine = UnusedCodeAnalyzer(graph)
    unused_res = unused_engine.analyze_unused()
    assert len(unused_res) > 0
    # old_code.py or legacy functions should be detected
    unused_names = [u["file_path"] for u in unused_res]
    assert any("old_code.py" in p for p in unused_names)

    # 5. Report Generation
    report_data = ReportGenerator.compile_report(
        scan_data=scan_info,
        graph_data={"total_nodes": graph.number_of_nodes, "total_edges": graph.number_of_edges},
        unused_candidates=unused_res,
        top_hubs=[],
    )
    pdf_out = ReportGenerator.export(report_data, "pdf")
    docx_out = ReportGenerator.export(report_data, "docx")
    csv_out = ReportGenerator.export(report_data, "csv")

    assert len(pdf_out) > 50
    assert len(docx_out) > 50
    assert len(csv_out) > 50


def test_javascript_and_web_impact_pipeline():
    js_zip = SAMPLES_DIR / "javascript_demo.zip"
    assert js_zip.exists()

    extracted = safe_extract_zip(js_zip)
    scanner = ProjectScanner(extracted)
    scan_info = scanner.scan()
    assert scan_info["total_files"] >= 3

    dep_analyzer = DependencyAnalyzer(extracted)
    graph = dep_analyzer.analyze(scan_info["files"])
    assert graph.number_of_nodes > 0

    impact_engine = ImpactAnalyzer(graph)
    # Test impact of a node and upstream dependencies
    nodes = list(graph.graph.nodes)
    assert len(nodes) > 0

    # Pick a node and verify impact_res structure
    target = nodes[0]
    res = impact_engine.analyze_impact(target)
    assert "total_affected" in res
    assert "upstream_dependencies" in res
    assert "upstream_count" in res
    assert isinstance(res["upstream_dependencies"], list)

