"""
impactx â€” ML-Based Code Change Impact and Unused Code Prediction System
Main Streamlit Application Entry Point with Glassmorphism Theme:
  - Navigation: About | Steps | Projects | Dashboard
  - Rich frosted glass UI with ambient cosmic mesh gradient
  - Zero cartoon emojis
"""

import sys
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Dict, Any

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import pandas as pd
import networkx as nx

from config.config import MODEL_METADATA_PATH
from src.utils.zip_handler import safe_extract_zip, SecurityError, CorruptedZipError
from src.analysis.project_scanner import ProjectScanner
from src.analysis.dependency_analyzer import DependencyAnalyzer
from src.analysis.impact_analyzer import ImpactAnalyzer
from src.analysis.unused_code_analyzer import UnusedCodeAnalyzer
from src.graph.graph_metrics import GraphMetricsEngine
from src.graph.cycle_detector import CycleDetector
from src.ml.model_loader import ModelRegistry
import importlib
import src.ai.gemini_engine
importlib.reload(src.ai.gemini_engine)
from src.ai.gemini_engine import GeminiEngine

import src.reporting.export_formats
import src.reporting.report_generator
importlib.reload(src.reporting.export_formats)
importlib.reload(src.reporting.report_generator)
from src.reporting.report_generator import ReportGenerator

import dashboard.components.theme
import dashboard.components.cards
importlib.reload(dashboard.components.theme)
importlib.reload(dashboard.components.cards)
from dashboard.components.theme import get_theme_css
from dashboard.components.cards import (
    render_platform_header,
    render_platform_header_content,
    render_metric_card,
    render_risk_badge,
    render_pipeline_card,
    render_capability_card,
    render_logo_svg,
    render_brand_icon,
    PIPELINE_STAGES_DATA,
    CORE_CAPABILITIES_DATA,
    UPLOAD_FEATURES_DATA,
)
from dashboard.components.graphs import (
    build_language_pie,
    build_roc_curve,
    build_feature_importance_bar,
    build_confusion_matrix_heatmap,
)
from dashboard.components.tables import (
    format_impact_table,
    format_unused_table,
    format_hubs_table,
    parse_entity_label,
)

# Page configuration - permanently dark and wide
st.set_page_config(
    page_title="impactx â€” Architecture Intelligence",
    page_icon="impactx",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run_project_analysis(target_dir: Path, project_name: str = ""):
    """Runs complete end-to-end analysis on target_dir and caches in session_state."""
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

    st.session_state["project_data"] = scan_info
    st.session_state["dep_graph"] = dep_graph
    st.session_state["metrics"] = metrics
    st.session_state["top_hubs"] = top_hubs
    st.session_state["cycles"] = cycles
    st.session_state["has_cycles"] = has_cycles
    st.session_state["unused_results"] = unused_results
    st.session_state["ai_arch_summary"] = None
    st.session_state["ai_impact_cache"] = {}
    st.session_state["ai_unused_cache"] = {}
    st.session_state["analysis_ready"] = True

def render_top_navbar(current_view: str, project_name: str = ""):
    """Streamlined top navigation bar. Shows About/Steps toggle only on intro views."""
    show_nav_links = current_view in ("about", "steps")

    if show_nav_links:
        c_brand, c_nav1, c_nav2 = st.columns(
            [6.6, 1.7, 1.7],
            vertical_alignment="center"
        )
    else:
        c_brand = st.container()

    with c_brand:
        proj_badge = (
            f'<span style="font-size: 11px; font-weight: 600; color: #10B981; margin-left: 8px; '
            f'background: rgba(16, 185, 129, 0.14); padding: 3px 9px; border-radius: 6px; '
            f'border: 1px solid rgba(16, 185, 129, 0.3); backdrop-filter: blur(8px); white-space: nowrap;">&#11044; {project_name}</span>'
            if project_name else ""
        )
        brand_icon_html = render_brand_icon(28)
        navbar_html = (
            f'<div style="display: flex; align-items: center; gap: 8px; margin: 0; padding: 0;">'
            f'{brand_icon_html}'
            f'<span style="font-size: 17px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.3px; line-height: 1;">impactx</span>'
            f'<span style="font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 4px; background: rgba(255, 255, 255, 0.06); color: #94A3B8; border: 1px solid rgba(255, 255, 255, 0.1); letter-spacing: 0.5px;">ML PLATFORM</span>'
            f'{proj_badge}'
            f'</div>'
        )
        st.markdown(navbar_html, unsafe_allow_html=True)

    if show_nav_links:
        with c_nav1:
            btn_type = "primary" if current_view == "about" else "secondary"
            if st.button("About", type=btn_type, key=f"nav_btn_about_{current_view}", use_container_width=True):
                st.session_state["current_view"] = "about"
                st.rerun()

        with c_nav2:
            btn_type = "primary" if current_view == "steps" else "secondary"
            if st.button("Steps", type=btn_type, key=f"nav_btn_steps_{current_view}", use_container_width=True):
                st.session_state["current_view"] = "steps"
                st.rerun()

    st.markdown('<div style="height: 1px; background: rgba(255, 255, 255, 0.08); margin: 6px 0 20px 0;"></div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# VIEW 1: ABOUT (PLATFORM INTELLIGENCE & CAPABILITIES)
# -------------------------------------------------------------

def render_about_view(project_name: str = ""):
    """View 1: About impactx platform and core intelligence capabilities."""
    render_top_navbar("about", project_name=project_name)

    # Hero Glass Card (Clean, Zero Glow)
    st.markdown("""
    <div style="text-align: center; padding: 32px 24px 22px 24px; background: #0E131F; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35); margin-bottom: 22px;">
        <div style="display: inline-block; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #94A3B8; background: rgba(255, 255, 255, 0.05); padding: 3px 10px; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 12px;">
            Architecture Intelligence &bull; Offline Sandboxed ML
        </div>
        <h1 style="font-size: 34px; font-weight: 800; color: #FFFFFF; line-height: 1.2; letter-spacing: -0.025em; margin: 0 0 10px 0;">
            Code Change Impact &amp; Architecture Intelligence
        </h1>
        <p style="font-size: 14px; color: #94A3B8; max-width: 740px; margin: 0 auto 18px auto; line-height: 1.6;">
            Analyze dependencies, simulate downstream blast radius before merging code, and identify unreferenced dead code across Python, JavaScript, TypeScript, HTML, and CSS repositories with machine learning.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Navigation CTA Row
    c_cta1, c_cta2, c_cta3 = st.columns([1, 2, 1])
    with c_cta2:
        if st.button("Proceed to Codebase Upload âž”", type="primary", key="about_to_projects_btn", use_container_width=True):
            st.session_state["prev_view"] = "about"
            st.session_state["current_view"] = "projects"
            st.rerun()

    # CORE CAPABILITIES SECTION (4-stage pipeline moved to Steps)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # SECTION 2: PLATFORM CORE CAPABILITIES
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: #818CF8;">System Architecture</div>
        <h2 style="font-size: 24px; font-weight: 800; color: #FFFFFF; margin: 4px 0 0 0;">Core Intelligence Capabilities</h2>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3, gap="medium")
    row1 = CORE_CAPABILITIES_DATA[:3]
    row2 = CORE_CAPABILITIES_DATA[3:]

    for col, cap_item in zip([col_c1, col_c2, col_c3], row1):
        with col:
            st.markdown(render_capability_card(**cap_item), unsafe_allow_html=True)

    if row2:
        st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
        _pad, col_r2a, col_r2b, _pad2 = st.columns([0.5, 1, 1, 0.5], gap="medium")
        for col, cap_item in zip([col_r2a, col_r2b], row2):
            with col:
                st.markdown(render_capability_card(**cap_item), unsafe_allow_html=True)

    # Footer CTA
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    c_bot1, c_bot2, c_bot3 = st.columns([1, 2, 1])
    with c_bot2:
        if st.button("Proceed to Codebase Upload âž”", type="primary", key="btn_about_footer_projects", use_container_width=True):
            st.session_state["prev_view"] = "about"
            st.session_state["current_view"] = "projects"
            st.rerun()

    # Footer
    st.markdown("""
    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding: 28px 0 16px 0; margin-top: 40px; text-align: center;">
        <div style="font-weight: 700; font-size: 13px; color: #FFFFFF; margin-bottom: 4px;">
            impactx &mdash; Enterprise Code Change Impact &amp; Architecture ML Platform
        </div>
        <div style="font-size: 12px; color: #64748B;">
            Local Offline Execution &bull; Multi-Language AST &bull; ML Blast Radius &amp; Dead Code Inference
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# VIEW 2: STEPS (PIPELINE & EXECUTION WORKFLOW)
# -------------------------------------------------------------

def render_steps_view(project_name: str = ""):
    """View 2: 4-Stage analysis pipeline and execution workflow."""
    render_top_navbar("steps", project_name=project_name)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 28px;">
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.4px; color: #818CF8;">Execution Workflow</div>
        <h1 style="font-size: 36px; font-weight: 800; color: #FFFFFF; margin: 4px 0 8px 0; letter-spacing: -0.02em;">
            4-Stage Analysis Pipeline
        </h1>
        <p style="font-size: 14px; color: #94A3B8; max-width: 680px; margin: 0 auto; line-height: 1.6;">
            How impactx transforms raw repository archives into predictive graph intelligence and actionable risk audits.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    for i, stage_item in enumerate(PIPELINE_STAGES_DATA):
        target_col = col_s1 if i % 2 == 0 else col_s2
        with target_col:
            st.markdown(render_pipeline_card(**stage_item), unsafe_allow_html=True)

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    c_st1, c_st2, c_st3 = st.columns([1.5, 2, 1.5])
    with c_st2:
        if st.button("Proceed to Codebase Upload âž”", type="primary", key="btn_steps_to_projects", use_container_width=True):
            st.session_state["prev_view"] = "steps"
            st.session_state["current_view"] = "projects"
            st.rerun()

    # Footer
    st.markdown("""
    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding: 28px 0 16px 0; margin-top: 40px; text-align: center;">
        <div style="font-weight: 700; font-size: 13px; color: #FFFFFF; margin-bottom: 4px;">
            impactx &mdash; Enterprise Code Change Impact &amp; Architecture ML Platform
        </div>
        <div style="font-size: 12px; color: #64748B;">
            Local Offline Execution &bull; Multi-Language AST &bull; ML Blast Radius &amp; Dead Code Inference
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# VIEW 3: PROJECTS (REPOSITORY INGESTION & UPLOAD)
# -------------------------------------------------------------

def render_projects_view(project_name: str = ""):
    """View 3: Clean enterprise repository upload & sandboxed code ingestion."""
    render_top_navbar("projects", project_name=project_name)

    # Back button shifted to the left side of the page
    c_back_left, _ = st.columns([1.5, 8.5])
    with c_back_left:
        target_back = st.session_state.get("prev_view", "about")
        back_label = "Back to Steps" if target_back == "steps" else "Back to About"
        if st.button(back_label, key="btn_projects_back_about", use_container_width=True):
            st.session_state["current_view"] = target_back
            st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Centered Ingestion Card Column
    _, col_center, _ = st.columns([1.5, 4.5, 1.5])

    with col_center:
        # Enterprise Card Container
        with st.container(border=True):
            # Centered Brand Header inside Card
            st.markdown(f"""
            <div style="text-align: center; padding: 12px 10px 14px 10px;">
                <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.09); margin-bottom: 12px;">
                    {render_logo_svg(size=24)}
                </div>
                <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 4px; letter-spacing: -0.02em;">Upload Codebase Archive</div>
                <div style="font-size: 13px; color: #94A3B8; max-width: 500px; margin: 0 auto; line-height: 1.5;">
                    Upload a <code>.zip</code> repository archive or specify a local directory path to begin offline AST parsing &amp; ML blast radius prediction.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if "ingest_mode_btn" not in st.session_state:
                st.session_state["ingest_mode_btn"] = "zip"

            # Clean Segmented Ingestion Switcher (Zero Red Underline)
            c_sw1, c_sw2 = st.columns(2)
            with c_sw1:
                is_zip = (st.session_state["ingest_mode_btn"] == "zip")
                btype = "primary" if is_zip else "secondary"
                if st.button("Upload Archive (.ZIP)", type=btype, key="btn_switch_zip", use_container_width=True):
                    st.session_state["ingest_mode_btn"] = "zip"
                    st.rerun()
            with c_sw2:
                is_dir = (st.session_state["ingest_mode_btn"] == "dir")
                btype = "primary" if is_dir else "secondary"
                if st.button("Direct Local Directory", type=btype, key="btn_switch_dir", use_container_width=True):
                    st.session_state["ingest_mode_btn"] = "dir"
                    st.rerun()

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            if st.session_state["ingest_mode_btn"] == "zip":
                upload_zip = st.file_uploader(
                    "Upload codebase ZIP archive",
                    type=["zip"],
                    key="projects_view_file_uploader",
                    label_visibility="collapsed",
                    help="Maximum upload limit: 1000 MB. Processed 100% offline inside local sandbox.",
                )

                # Clean, Monochromatic Neutral Format Pills
                st.markdown("""
                <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin: 14px 0 16px 0;">
                    <span style="background: rgba(255, 255, 255, 0.04); color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.08);">Python (.py)</span>
                    <span style="background: rgba(255, 255, 255, 0.04); color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.08);">JavaScript (.js, .jsx)</span>
                    <span style="background: rgba(255, 255, 255, 0.04); color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.08);">TypeScript (.ts, .tsx)</span>
                    <span style="background: rgba(255, 255, 255, 0.04); color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.08);">HTML5 (.html)</span>
                    <span style="background: rgba(255, 255, 255, 0.04); color: #94A3B8; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.08);">CSS3 (.css)</span>
                </div>
                """, unsafe_allow_html=True)

                if upload_zip is not None:
                    file_size_mb = len(upload_zip.getvalue()) / (1024 * 1024)
                    st.markdown(f"""
                    <div style="padding: 14px 18px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;">
                        <div style="color: #10B981; font-weight: 600; font-size: 13px; display: flex; align-items: center; gap: 8px;">
                            <span>âœ“</span>
                            <span>Archive Ready: <strong>{upload_zip.name}</strong> ({file_size_mb:.1f} MB)</span>
                        </div>
                        <span style="font-size: 11px; color: #6EE7B7; background: rgba(16, 185, 129, 0.2); padding: 3px 10px; border-radius: 4px; font-weight: 700;">READY</span>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Extract & Run Full Analysis on {upload_zip.name}", type="primary", use_container_width=True, key="btn_upload_projects_page"):
                        progress_bar = st.progress(0, text="1/4 Initializing local sandbox extraction...")
                        temp_dir = Path(tempfile.mkdtemp(prefix="impactx_upload_"))
                        zip_temp_path = temp_dir / upload_zip.name
                        with open(zip_temp_path, "wb") as f:
                            f.write(upload_zip.getbuffer())

                        progress_bar.progress(25, text="2/4 Safely extracting source code files (bypassing node_modules/)...")
                        try:
                            extracted_path = safe_extract_zip(zip_temp_path)
                            proj_clean_name = upload_zip.name.rsplit(".", 1)[0]
                            progress_bar.progress(60, text="3/4 Parsing multi-language ASTs & building NetworkX topology...")
                            run_project_analysis(extracted_path, project_name=proj_clean_name)
                            progress_bar.progress(100, text="4/4 Analysis complete! Redirecting to Dashboard...")
                            st.session_state["current_view"] = "dashboard"
                            st.rerun()
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")

            else:
                st.markdown("""
                <div style="font-size: 13px; color: #94A3B8; margin-bottom: 12px; text-align: center;">
                    Enter a local filesystem directory or .zip path for instantaneous offline analysis.
                </div>
                """, unsafe_allow_html=True)

                local_path_input = st.text_input(
                    "Local Repository Path",
                    placeholder=r"e.g. C:\Users\eZee\Desktop\task2 or C:\Users\eZee\Desktop\task2.zip",
                    label_visibility="collapsed",
                    key="input_local_repo_path",
                )

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                if st.button("Scan & Ingest Local Path", type="primary", use_container_width=True, key="btn_ingest_local_path"):
                    raw_input = (local_path_input or "").strip().strip('"').strip("'")
                    if not raw_input:
                        st.warning("Please enter a valid local directory or .zip file path.")
                    else:
                        target_p = Path(raw_input)
                        if not target_p.exists():
                            st.error(f"Path not found on disk: `{target_p}`")
                        else:
                            with st.spinner(f"Scanning and analyzing `{target_p.name}`..."):
                                try:
                                    if target_p.is_file() and target_p.suffix.lower() == ".zip":
                                        extracted = safe_extract_zip(target_p)
                                        run_project_analysis(extracted, project_name=target_p.stem)
                                    elif target_p.is_dir():
                                        run_project_analysis(target_p, project_name=target_p.name)
                                    else:
                                        st.error("Provided path must be a folder directory or a .zip file.")
                                        target_p = None
                                    if target_p:
                                        st.session_state["current_view"] = "dashboard"
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Analysis failed: {e}")

        # Architectural Pipeline Feature Cards below centered card
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        c_f1, c_f2, c_f3 = st.columns(3)
        for i, feat_item in enumerate(UPLOAD_FEATURES_DATA):
            target_col = c_f1 if i == 0 else (c_f2 if i == 1 else c_f3)
            with target_col:
                st.markdown(render_capability_card(**feat_item), unsafe_allow_html=True)

# -------------------------------------------------------------
# VIEW 4: DASHBOARD (PROJECT ANALYSIS & METRICS)
# -------------------------------------------------------------

def render_dashboard_view(scan_info: Dict[str, Any], dep_graph, metrics: Dict[str, Any], top_hubs: List[Dict[str, Any]], cycles: List[List[str]], has_cycles: bool, unused_results: List[Dict[str, Any]]):
    """View 4: Interactive project intelligence dashboard in Glassmorphic styling."""
    current_proj = scan_info.get("project_name", "")
    render_top_navbar("dashboard", project_name=current_proj)

    # Empty State Guard if no codebase has been uploaded yet
    if not scan_info or not dep_graph or dep_graph.number_of_nodes == 0:
        st.markdown("""
        <div style="text-align: center; padding: 48px 24px; background: #0E131F; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; max-width: 600px; margin: 36px auto; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);">
            <div style="width: 52px; height: 52px; margin: 0 auto 16px auto; border-radius: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; font-size: 24px;">&#128193;</div>
            <h2 style="font-size: 22px; font-weight: 800; color: #FFFFFF; margin: 0 0 8px 0;">No Codebase Analyzed Yet</h2>
            <p style="font-size: 13px; color: #94A3B8; max-width: 460px; margin: 0 auto 24px auto; line-height: 1.6;">
                Please upload your repository ZIP archive in the Projects section to begin AST parsing, dependency graph modeling, ML blast radius prediction, and dead code detection.
            </p>
        </div>
        """, unsafe_allow_html=True)
        c_emp1, c_emp2, c_emp3 = st.columns([1, 1.6, 1])
        with c_emp2:
            if st.button("Go to Upload Codebase", type="primary", key="btn_empty_to_upload", use_container_width=True):
                st.session_state["current_view"] = "projects"
                st.rerun()
        return

    # Navigation Back Row & Active Codebase HUD Telemetry Bar
    c_hud_back, c_hud_info = st.columns([1.2, 5.8], vertical_alignment="center")
    with c_hud_back:
        if st.button("Back to Upload", key="btn_dash_back_projects", use_container_width=True):
            st.session_state["current_view"] = "projects"
            st.rerun()
    with c_hud_info:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 18px; border-radius: 12px; background: #0E131F; border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);">
            <div style="font-size: 13px; font-weight: 700; color: #FFFFFF; display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #10B981;"></span>
                Active Codebase: <span style="color: #E2E8F0; font-weight: 700;">{current_proj}</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; font-weight: 500;">
                {scan_info.get('total_files', 0)} Files &bull; {scan_info.get('total_code_lines', 0):,} Lines of Code &bull; {dep_graph.number_of_nodes} Graph Entities &bull; {dep_graph.number_of_edges} Dependencies
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Modern Segmented Toolbar Navigation
    DASHBOARD_NAV_TABS = [
        {"id": "overview", "label": "Overview & Metrics", "icon": "📊"},
        {"id": "structure", "label": "Project Structure", "icon": "📁"},
        {"id": "impact", "label": "Impact Analysis", "icon": "⚡"},
        {"id": "unused", "label": "Dead Code", "icon": "🔍"},
        {"id": "ml", "label": "ML Explainability", "icon": "🧠"},
        {"id": "reports", "label": "Audit Reports", "icon": "📑"},
    ]
    if "dash_active_tab_id" not in st.session_state:
        st.session_state["dash_active_tab_id"] = "overview"

    with st.container(border=True):
        c_nav_tabs = st.columns(6)
        for idx, tab_info in enumerate(DASHBOARD_NAV_TABS):
            is_active = (st.session_state["dash_active_tab_id"] == tab_info["id"])
            b_type = "primary" if is_active else "secondary"
            btn_title = f"{tab_info['icon']}  {tab_info['label']}"
            with c_nav_tabs[idx]:
                if st.button(btn_title, type=b_type, key=f"dash_tab_btn_{tab_info['id']}", use_container_width=True):
                    st.session_state["dash_active_tab_id"] = tab_info["id"]
                    st.rerun()

    active_tab = st.session_state["dash_active_tab_id"]
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 1: OVERVIEW & ARCHITECTURE
    # -------------------------------------------------------------
    if active_tab == "overview":
        st.markdown(f"### Project Overview: `{current_proj}`")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(render_metric_card("Total Files", scan_info.get("total_files", 0), "Analyzed in codebase"), unsafe_allow_html=True)
        with c2:
            st.markdown(render_metric_card("Lines of Code", f"{scan_info.get('total_code_lines', 0):,}", f"Total lines: {scan_info.get('total_lines', 0):,}"), unsafe_allow_html=True)
        with c3:
            st.markdown(render_metric_card("Dependencies", dep_graph.number_of_edges, f"Entities mapped: {dep_graph.number_of_nodes}"), unsafe_allow_html=True)
        with c4:
            high_risk_unused = sum(1 for u in unused_results if u.get("risk_level") == "HIGH")
            st.markdown(render_metric_card("Dead Code Candidates", len(unused_results), f"High Risk: {high_risk_unused}"), unsafe_allow_html=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        col_pie, col_health = st.columns([1, 1])
        with col_pie:
            st.markdown("#### Language Composition")
            lang_dist = scan_info.get("language_distribution", {})
            if lang_dist:
                fig_pie = build_language_pie(lang_dist, theme="dark")
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No supported languages detected.")

        with col_health:
            st.markdown("#### Architectural Coupling & Health")
            h1, h2 = st.columns(2)
            with h1:
                st.markdown(render_metric_card("Graph Entities", dep_graph.number_of_nodes, "Total components mapped"), unsafe_allow_html=True)
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                max_in = max([m.get("in_degree", 0) for m in metrics.values()], default=0)
                st.markdown(render_metric_card("Max In-Degree", max_in, "Peak dependents on single component"), unsafe_allow_html=True)
            with h2:
                avg_deps = round(dep_graph.number_of_edges / max(1, dep_graph.number_of_nodes), 2)
                st.markdown(render_metric_card("Avg Coupling", avg_deps, "Dependencies per entity"), unsafe_allow_html=True)
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                cycle_status = "0 (Clean DAG)" if not has_cycles else f"{len(cycles)} Detected"
                st.markdown(render_metric_card("Cycles", cycle_status, "Circular dependency count"), unsafe_allow_html=True)

        st.divider()

        # Groq AI Architectural Assessment (if available)
        if GeminiEngine.is_available():
            with st.expander("Groq AI Architectural Assessment & Risk Intelligence", expanded=True):
                if st.session_state.get("ai_arch_summary"):
                    st.markdown(st.session_state["ai_arch_summary"])
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    if st.button("Re-generate AI Assessment", key="btn_regen_ai_arch"):
                        with st.spinner("Analyzing codebase topology with Groq AI..."):
                            summary = GeminiEngine.generate_architecture_summary(scan_info, metrics, top_hubs, cycles)
                            st.session_state["ai_arch_summary"] = summary
                            st.session_state["current_view"] = "dashboard"
                            st.query_params["view"] = "dashboard"
                            st.rerun()
                else:
                    st.caption("Generate an executive architectural assessment, hotspot risk analysis, and change isolation recommendations.")
                    if st.button("Generate AI Architectural Intelligence", key="btn_gen_ai_arch"):
                        with st.spinner("Analyzing codebase topology with Groq AI..."):
                            summary = GeminiEngine.generate_architecture_summary(scan_info, metrics, top_hubs, cycles)
                            st.session_state["ai_arch_summary"] = summary
                            st.session_state["current_view"] = "dashboard"
                            st.query_params["view"] = "dashboard"
                            st.rerun()

            st.divider()

        # Top Architectural Hubs
        with st.expander("Top Architectural Hubs (Highest Risk Components)", expanded=True):
            st.caption("Components with highest PageRank centrality and incoming dependents. Changes to these components produce the largest downstream ripple effect.")
            if top_hubs:
                col_sel, col_stat = st.columns([3, 1], vertical_alignment="bottom")
                with col_sel:
                    hub_labels = [
                        f"{parse_entity_label(h['id'])[0]} ({str(h.get('entity_type', 'file')).upper()}) â€” Dependents: {h.get('in_degree', 0)}"
                        for h in top_hubs
                    ]
                    selected_hub_idx = st.selectbox(
                        "Inspect Specific Hub from Dropdown:",
                        range(len(hub_labels)),
                        format_func=lambda i: hub_labels[i],
                    )

                chosen = top_hubs[selected_hub_idx]
                d_name, f_path, _ = parse_entity_label(chosen["id"])

                with col_stat:
                    st.metric(label="PageRank Centrality", value=f"{chosen.get('pagerank', 0.0):.4f}")

                # Hub Detail Card
                st.markdown(f"""
                <div style="background: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px 22px; margin: 10px 0 18px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                        <div>
                            <span style="font-size: 15px; font-weight: 700; color: #F1F5F9; letter-spacing: -0.2px;">{d_name}</span>
                            <span style="background: rgba(255,255,255,0.06); color: #94A3B8; border: 1px solid rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 5px; font-size: 10.5px; font-weight: 600; margin-left: 8px; font-family: 'JetBrains Mono', monospace;">{str(chosen.get('entity_type', 'file')).upper()}</span>
                            <div style="font-size: 11.5px; color: #64748B; font-family: 'JetBrains Mono', monospace; margin-top: 6px;">{f_path}</div>
                        </div>
                        <div style="display: flex; gap: 12px;">
                            <div style="text-align: center; background: rgba(255,255,255,0.04); padding: 10px 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                                <div style="font-size: 10px; color: #94A3B8; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 4px;">Incoming</div>
                                <div style="font-size: 24px; font-weight: 800; color: #F1F5F9; line-height: 1;">{chosen.get('in_degree', 0)}</div>
                            </div>
                            <div style="text-align: center; background: rgba(255,255,255,0.04); padding: 10px 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                                <div style="font-size: 10px; color: #94A3B8; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 4px;">Outgoing</div>
                                <div style="font-size: 24px; font-weight: 800; color: #F1F5F9; line-height: 1;">{chosen.get('out_degree', 0)}</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                df_hubs = format_hubs_table(top_hubs)
                st.dataframe(
                    df_hubs,
                    column_config={
                        "Component": st.column_config.TextColumn("Component", width="medium"),
                        "Type": st.column_config.TextColumn("Type", width="small"),
                        "PageRank": st.column_config.NumberColumn("PageRank", format="%.4f", width="small"),
                        "Dependents (In)": st.column_config.NumberColumn("Dependents (In)", format="%d", width="small"),
                        "Dependencies (Out)": st.column_config.NumberColumn("Dependencies (Out)", format="%d", width="small"),
                        "File Location": st.column_config.TextColumn("File Location", width="large"),
                    },
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No architectural hubs identified.")

    # -------------------------------------------------------------
    # TAB 2: PROJECT STRUCTURE
    # -------------------------------------------------------------
    elif active_tab == "structure":
        st.markdown("### Project File Inventory & AST Breakdown")
        st.caption("Complete breakdown of source files, lines of code, and architectural categories.")
        files = scan_info.get("files", [])

        # Summary Metrics
        sf1, sf2, sf3 = st.columns(3)
        with sf1:
            st.markdown(render_metric_card("Repository Files", len(files), "Source files cataloged"), unsafe_allow_html=True)
        with sf2:
            st.markdown(render_metric_card("Code Lines (LOC)", f"{scan_info.get('total_code_lines', 0):,}", "Effective code lines"), unsafe_allow_html=True)
        with sf3:
            detected_langs = len([l for l in scan_info.get("language_distribution", {}) if l != "Unknown"])
            st.markdown(render_metric_card("Languages Detected", detected_langs, "Multi-language AST parsers"), unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        col_f1, col_f2 = st.columns([3, 1], vertical_alignment="bottom")
        with col_f1:
            search_query = st.text_input("Search files by path or name:", "")
        with col_f2:
            langs = ["All"] + sorted(list(set(f["language"] for f in files if f["language"] != "Unknown")))
            selected_lang = st.selectbox("Filter by language:", langs)

        filtered_files = files
        if search_query:
            filtered_files = [f for f in filtered_files if search_query.lower() in f["path"].lower()]
        if selected_lang != "All":
            filtered_files = [f for f in filtered_files if f["language"] == selected_lang]

        df_files = pd.DataFrame([
            {
                "File Path": f["path"],
                "Language": f["language"],
                "Category": f["category"].upper(),
                "Code LOC": int(f["code_lines"]),
                "Total Lines": int(f["total_lines"]),
                "File Size": f"{f['size_bytes'] / 1024:.1f} KB",
            }
            for f in filtered_files
        ])

        st.dataframe(
            df_files,
            column_config={
                "File Path": st.column_config.TextColumn("File Path", width="large"),
                "Language": st.column_config.TextColumn("Language", width="small"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Code LOC": st.column_config.NumberColumn("Code LOC", format="%d", width="small"),
                "Total Lines": st.column_config.NumberColumn("Total Lines", format="%d", width="small"),
                "File Size": st.column_config.TextColumn("File Size", width="small"),
            },
            use_container_width=True,
            hide_index=True,
        )

    # -------------------------------------------------------------
    # TAB 3: IMPACT ANALYSIS
    # -------------------------------------------------------------
    elif active_tab == "impact":
        st.markdown("### Change Impact & Blast Radius Prediction")
        st.caption("Select a component to predict downstream blast radius, transitive affected entities, and ML risk scores.")

        all_nodes = sorted(list(dep_graph.graph.nodes()))
        if not all_nodes:
            st.info("No components available for impact analysis.")
        else:
            hub_candidates = []
            for n in all_nodes:
                in_deg = dep_graph.graph.in_degree(n)
                if in_deg > 0:
                    hub_candidates.append((n, in_deg))
            hub_candidates.sort(key=lambda x: x[1], reverse=True)
            top_impact_hubs = [item[0] for item in hub_candidates[:6]]

            if "selected_impact_target" not in st.session_state:
                if top_impact_hubs:
                    st.session_state["selected_impact_target"] = top_impact_hubs[0]
                else:
                    st.session_state["selected_impact_target"] = all_nodes[0]

            if top_impact_hubs:
                st.markdown("<div style='font-size: 11px; font-weight: 700; color: #A5B4FC; text-transform: uppercase; letter-spacing: 0.9px; margin-bottom: 6px;'>Recommended High-Impact Hubs (Highest Blast Radius):</div>", unsafe_allow_html=True)
                chip_cols = st.columns(min(len(top_impact_hubs), 5))
                for idx_c, hub_name in enumerate(top_impact_hubs[:5]):
                    short_name = hub_name.split("/")[-1]
                    ref_count = dep_graph.graph.in_degree(hub_name)
                    with chip_cols[idx_c]:
                        if st.button(f"{short_name} ({ref_count} refs)", key=f"quick_hub_{idx_c}", use_container_width=True):
                            st.session_state["selected_impact_target"] = hub_name
                            st.rerun()

            current_target = st.session_state.get("selected_impact_target", all_nodes[0])
            if current_target not in all_nodes:
                current_target = all_nodes[0]
            current_idx = all_nodes.index(current_target)

            selected_component = st.selectbox(
                "Select Target Component to Modify:",
                all_nodes,
                index=current_idx,
                key="impact_target_select",
            )
            if selected_component != st.session_state.get("selected_impact_target"):
                st.session_state["selected_impact_target"] = selected_component

            impact_engine = ImpactAnalyzer(dep_graph)
            impact_res = impact_engine.analyze_impact(selected_component)

            m1, m2, m3, m4, m5 = st.columns(5)
            with m1:
                st.markdown(render_metric_card("Blast Radius", impact_res["total_affected"], "Downstream components"), unsafe_allow_html=True)
            with m2:
                st.markdown(render_metric_card("Direct (Level 1)", impact_res["direct_count"], "Immediate dependents"), unsafe_allow_html=True)
            with m3:
                st.markdown(render_metric_card("Transitive (Level 2+)", impact_res["indirect_count"], "Cascade ripple"), unsafe_allow_html=True)
            with m4:
                st.markdown(render_metric_card("High Risk", impact_res["high_risk_count"], "Probability >= 70%"), unsafe_allow_html=True)
            with m5:
                st.markdown(render_metric_card("Prerequisites", impact_res.get("upstream_count", 0), "Required upstream dependencies"), unsafe_allow_html=True)

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            if impact_res["affected_components"]:
                st.markdown(f"#### Downstream Blast Radius ({impact_res['total_affected']} Affected Components)")
                df_impact = format_impact_table(impact_res["affected_components"])
                st.dataframe(
                    df_impact,
                    column_config={
                        "Component": st.column_config.TextColumn("Affected Component", width="medium"),
                        "Type": st.column_config.TextColumn("Type", width="small"),
                        "Impact Level": st.column_config.TextColumn("Impact Level", width="small"),
                        "Hops": st.column_config.NumberColumn("Distance (Hops)", format="%d", width="small"),
                        "Impact Probability": st.column_config.ProgressColumn(
                            "Impact Probability",
                            format="%.1f%%",
                            min_value=0.0,
                            max_value=1.0,
                            width="medium",
                        ),
                        "Risk Tier": st.column_config.TextColumn("Risk Tier", width="small"),
                        "Key Driver": st.column_config.TextColumn("Key Driver", width="medium"),
                        "File Location": st.column_config.TextColumn("File Location", width="large"),
                    },
                    use_container_width=True,
                    hide_index=True,
                )

                st.markdown("#### Dependency Ripple Paths")
                for aff in impact_res["affected_components"][:6]:
                    path_str = " âž” ".join(aff["path"])
                    st.markdown(f"""
                    <div style="background: rgba(16, 21, 38, 0.5); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 14px; margin-bottom: 6px; font-size: 13px;">
                        <span style="font-weight: 700; color: #FFFFFF;">{aff['component']}</span>
                        <span style="color: #818CF8; font-size: 11px; margin-left: 6px;">({aff['level']})</span>:
                        <code style="background: rgba(255,255,255,0.06); color: #C7D2FE; margin-left: 6px;">{path_str}</code>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(
                    f"Terminal Component: No downstream components depend on `{selected_component}` (Blast Radius = 0). "
                    "Changes to this file will not break other files in the codebase."
                )

            upstream_list = impact_res.get("upstream_dependencies", [])
            if upstream_list:
                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                st.markdown(f"#### Upstream Prerequisites ({len(upstream_list)} components required by `{selected_component.split('/')[-1]}`)")
                df_up = pd.DataFrame([
                    {
                        "Prerequisite Component": d["component"],
                        "Type": d["type"],
                        "Language": d["language"],
                        "Relationship": d["relationship"],
                    }
                    for d in upstream_list
                ])
                st.dataframe(df_up, use_container_width=True, hide_index=True)

            if GeminiEngine.is_available():
                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                with st.expander(f"Groq AI Semantic Blast Radius & Verification: `{selected_component.split('/')[-1]}`", expanded=False):
                    cache_key = f"impact_{selected_component}"
                    ai_cache = st.session_state.get("ai_impact_cache", {})
                    if cache_key in ai_cache:
                        st.markdown(ai_cache[cache_key])
                        if st.button("Re-analyze Impact with Groq", key=f"regen_{cache_key}"):
                            with st.spinner(f"Reasoning blast radius for {selected_component}..."):
                                reasoning = GeminiEngine.explain_impact(selected_component, impact_res)
                                ai_cache[cache_key] = reasoning
                                st.session_state["ai_impact_cache"] = ai_cache
                                st.session_state["current_view"] = "dashboard"
                                st.query_params["view"] = "dashboard"
                                st.rerun()
                    else:
                        st.caption("Ask Groq AI to reason through downstream consumer breakage and recommend targeted regression tests.")
                        if st.button("Reason Blast Radius with Groq", key=f"btn_{cache_key}"):
                            with st.spinner(f"Analyzing semantic impact of modifying {selected_component}..."):
                                reasoning = GeminiEngine.explain_impact(selected_component, impact_res)
                                ai_cache[cache_key] = reasoning
                                st.session_state["ai_impact_cache"] = ai_cache
                                st.session_state["current_view"] = "dashboard"
                                st.query_params["view"] = "dashboard"
                                st.rerun()

    # -------------------------------------------------------------
    # TAB 4: UNUSED CODE
    # -------------------------------------------------------------
    elif active_tab == "unused":
        st.markdown("### Dead Code & Unreferenced Entity Detection")
        st.caption("Components with zero or minimal incoming references evaluated with graph PageRank and machine learning non-use confidence scores.")

        col_u1, col_u2 = st.columns([1, 1], vertical_alignment="bottom")
        with col_u1:
            risk_filter = st.multiselect(
                "Filter by Risk Tier",
                options=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                default=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                help="Only show candidates at or above selected risk tier",
            )
        with col_u2:
            type_filter = st.multiselect(
                "Filter by Entity Type",
                options=["file", "function", "class"],
                default=["file", "function", "class"],
            )

        filtered_unused = [
            u for u in unused_results
            if u.get("risk_level", "LOW") in risk_filter
            and u.get("type", "file") in type_filter
        ]

        if filtered_unused:
            df_unused = pd.DataFrame([
                {
                    "Component": u["name"],
                    "Type": str(u.get("type", "file")).upper(),
                    "File": u.get("file_path", ""),
                    "References": u.get("reference_count", 0),
                    "Confidence": f"{u.get('unused_probability', 0):.1%}",
                    "Risk Tier": u.get("risk_level", "LOW"),
                    "Evidence": (u.get("reasons") or ["No incoming references"])[0],
                }
                for u in filtered_unused
            ])
            st.dataframe(
                df_unused,
                use_container_width=True,
                hide_index=True,
            )

            if GeminiEngine.is_available():
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                cache_key = f"unused_{len(filtered_unused)}_{'_'.join(sorted(risk_filter))}_{'_'.join(sorted(type_filter))}"
                ai_cache = st.session_state.setdefault("ai_unused_cache", {})
                filter_ctx = {
                    "risk_levels": risk_filter,
                    "entity_types": type_filter,
                    "total_count": len(filtered_unused),
                }

                with st.expander(f"Groq AI Dead Code Advisory & Pruning Protocol ({len(filtered_unused)} Candidates)", expanded=(cache_key in ai_cache)):
                    if cache_key in ai_cache:
                        st.markdown(ai_cache[cache_key])
                        if st.button("Re-evaluate Table Pruning Safety", key=f"regen_{cache_key}"):
                            with st.spinner(f"Auditing all {len(filtered_unused)} table candidates with Groq AI..."):
                                adv = GeminiEngine.explain_unused_code(filtered_unused, filter_context=filter_ctx)
                                ai_cache[cache_key] = adv
                                st.session_state["ai_unused_cache"] = ai_cache
                                st.session_state["current_view"] = "dashboard"
                                st.query_params["view"] = "dashboard"
                                st.rerun()
                    else:
                        st.caption(f"Audit all {len(filtered_unused)} components with Groq AI to classify framework entry points, active references, and safe-to-prune dead code.")
                        if st.button(f"Evaluate Pruning Safety for Table Candidates ({len(filtered_unused)} items)", key=f"btn_{cache_key}"):
                            with st.spinner(f"Auditing all {len(filtered_unused)} table candidates with Groq AI..."):
                                adv = GeminiEngine.explain_unused_code(filtered_unused, filter_context=filter_ctx)
                                ai_cache[cache_key] = adv
                                st.session_state["ai_unused_cache"] = ai_cache
                                st.session_state["current_view"] = "dashboard"
                                st.query_params["view"] = "dashboard"
                                st.rerun()
        else:
            st.info("No unused code candidates match the current filter.")

    # -------------------------------------------------------------
    # TAB 5: ML EXPLAINABILITY & CALIBRATION
    # -------------------------------------------------------------
    elif active_tab == "ml":
        st.markdown("### Machine Learning Model Calibration & Explainability")
        st.caption("Insights into feature attribution weights, ROC curve calibration, and decision matrices.")

        metadata = ModelRegistry.get_metadata()
        if metadata:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("#### Impact Model Feature Importance")
                impact_imp = metadata.get("impact_model", {}).get("feature_importance", {})
                if impact_imp:
                    fig_imp = build_feature_importance_bar(impact_imp, theme="dark")
                    st.plotly_chart(fig_imp, use_container_width=True)
            with col_m2:
                st.markdown("#### Dead Code Feature Importance")
                unused_imp = metadata.get("unused_model", {}).get("feature_importance", {})
                if unused_imp:
                    fig_un = build_feature_importance_bar(unused_imp, theme="dark")
                    st.plotly_chart(fig_un, use_container_width=True)

            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

            # ROC Curve and Confusion Matrix
            col_roc, col_cm = st.columns(2)
            with col_roc:
                st.markdown("#### Model Calibration (ROC Curve)")
                impact_model_meta = metadata.get("impact_model", {})
                roc_data = impact_model_meta.get("roc_curve")
                auc_score = impact_model_meta.get("roc_auc", 0.0)
                if roc_data:
                    fig_roc = build_roc_curve(roc_data, auc_score, theme="dark")
                    st.plotly_chart(fig_roc, use_container_width=True)
                else:
                    st.info("ROC calibration curve available after model training.")

            with col_cm:
                st.markdown("#### Decision Boundaries (Confusion Matrix)")
                cm_data = impact_model_meta.get("confusion_matrix")
                if cm_data:
                    fig_cm = build_confusion_matrix_heatmap(cm_data, theme="dark")
                    st.plotly_chart(fig_cm, use_container_width=True)
                else:
                    st.info("Confusion matrix available after model training.")
        else:
            st.warning("Model metadata is not loaded. Train models via `python training/train_models.py`.")

    # -------------------------------------------------------------
    # TAB 6: AUDIT REPORTS
    # -------------------------------------------------------------
    elif active_tab == "reports":
        st.markdown("### Architectural Audit Reports & Export")
        st.caption("Generate complete project audit documentation and download in structured formats.")

        report_data = ReportGenerator.compile_report(
            scan_data=scan_info,
            graph_data={
                "total_nodes": dep_graph.number_of_nodes,
                "total_edges": dep_graph.number_of_edges,
                "has_cycles": has_cycles,
                "cycles": cycles,
            },
            unused_candidates=unused_results,
            top_hubs=top_hubs,
        )

        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp1:
            pdf_bytes = ReportGenerator.export(report_data, "pdf")
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=f"impactx_audit_report_{scan_info.get('project_name', 'project')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with col_exp2:
            docx_bytes = ReportGenerator.export(report_data, "docx")
            st.download_button(
                label="Download Word Report (.docx)",
                data=docx_bytes,
                file_name=f"impactx_audit_report_{scan_info.get('project_name', 'project')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with col_exp3:
            csv_report = ReportGenerator.export(report_data, "csv")
            st.download_button(
                label="Download CSV Report",
                data=csv_report,
                file_name=f"impactx_report_{scan_info.get('project_name', 'project')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown("#### Audit Report Preview")
        st.json({
            "project": report_data["project_name"],
            "timestamp": report_data["timestamp"],
            "total_files": report_data["total_files"],
            "total_code_lines": report_data["total_code_lines"],
            "dependencies_count": report_data["total_dependencies"],
            "dead_code_candidates": len(report_data["unused_candidates"]),
            "circular_dependencies": report_data["cycles_count"],
        })

# -------------------------------------------------------------
# MAIN APPLICATION CONTROLLER
# -------------------------------------------------------------

def main():
    # Lock theme permanently to dark
    st.session_state["theme"] = "dark"
    st.markdown(get_theme_css("dark"), unsafe_allow_html=True)

    # View state initialization: about -> projects -> dashboard
    if "current_view" not in st.session_state:
        initial_view = "about"
        if "view" in st.query_params:
            req_v = st.query_params.get("view")
            if req_v in ("about", "steps", "projects", "dashboard"):
                initial_view = req_v
        st.session_state["current_view"] = initial_view

    # Ensure no demo project is retained in session state
    curr_proj = st.session_state.get("project_data", {}).get("project_name", "")
    if any(demo_term in curr_proj.lower() for demo_term in ["demo", "sample", "reference"]):
        st.session_state["project_data"] = {}
        st.session_state["dep_graph"] = None
        st.session_state["metrics"] = {}
        st.session_state["top_hubs"] = []
        st.session_state["cycles"] = []
        st.session_state["has_cycles"] = False
        st.session_state["unused_results"] = []
        st.session_state["analysis_ready"] = False

    current_view = st.session_state.get("current_view", "about")
    scan_info = st.session_state.get("project_data", {})
    current_proj = scan_info.get("project_name", "")

    # Sidebar navigation & engine status
    with st.sidebar:
        sidebar_logo_svg = render_logo_svg(22)
        st.markdown(f"""
        <div class="sidebar-brand-card">
            <div class="sidebar-brand-logo">{sidebar_logo_svg}</div>
            <div>
                <div class="sidebar-brand-title">impactx</div>
                <div class="sidebar-brand-sub">ML Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if current_view != "about":
            if st.button("Start Over (About)", key="sb_btn_reset_about", use_container_width=True):
                st.session_state["current_view"] = "about"
                st.rerun()

        st.divider()

        gemini_active = GeminiEngine.is_available()
        gemini_badge = '<div style="font-size: 11px; color: #10B981; margin-top: 4px; font-weight: 600;">Groq AI Connected (Resilient Cascade)</div>' if gemini_active else ""

        st.markdown(f"""
        <div style="padding: 14px; border-radius: 12px; background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="font-size: 12px; font-weight: 700; color: #FFFFFF; display: flex; align-items: center;">
                <span class="status-dot"></span> Engine Online
            </div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">
                Models: XGBoost &amp; Random Forest
            </div>
            {gemini_badge}
            <div style="font-size: 11px; color: #64748B; margin-top: 2px;">
                impactx v2.1 (Glass Edition)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # ROUTE TO CURRENT VIEW
    # -------------------------------------------------------------
    if current_view == "about":
        render_about_view(project_name=current_proj)
    elif current_view == "steps":
        render_steps_view(project_name=current_proj)
    elif current_view == "projects":
        render_projects_view(project_name=current_proj)
    elif current_view == "dashboard":
        scan_info = st.session_state.get("project_data", {})
        dep_graph = st.session_state.get("dep_graph")
        metrics = st.session_state.get("metrics", {})
        top_hubs = st.session_state.get("top_hubs", [])
        cycles = st.session_state.get("cycles", [])
        has_cycles = st.session_state.get("has_cycles", False)
        unused_results = st.session_state.get("unused_results", [])
        render_dashboard_view(scan_info, dep_graph, metrics, top_hubs, cycles, has_cycles, unused_results)
    else:
        render_about_view(project_name=current_proj)

if __name__ == "__main__":
    main()

