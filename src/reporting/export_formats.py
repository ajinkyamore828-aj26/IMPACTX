"""
Comprehensive, Enterprise-Grade Export Formats for impactx:
- PDF (Publication-grade ReportLab document with NumberedCanvas, cover banner, KPI scorecard, language breakdown, full hubs table, dead code inventory, circular cycle audit, and refactoring protocol)
- Word DOCX (Professional enterprise document with header/footer, 8-KPI grid, styled tables, risk colors)
- CSV (Comprehensive multi-section tabular export of all graph metrics, hubs, and pruning inventory)
- HTML (Self-contained dark glassmorphic report matching impactx UI with print stylesheet)
- JSON (Structured audit manifest)
"""

import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, Optional, List

def _break_path(text: str) -> str:
    """Inserts zero-width spaces after slashes, backslashes, dots, and underscores for clean wrapping."""
    if not text:
        return ""
    return str(text).replace("/", "/​").replace("\\", "\\​").replace(".", ".​").replace("_", "_​")

def export_to_json(data: Dict[str, Any], output_path: Optional[Path] = None) -> str:
    """Exports analysis data to formatted JSON."""
    json_str = json.dumps(data, indent=2, default=str)
    if output_path:
        Path(output_path).write_text(json_str, encoding="utf-8")
    return json_str

def export_to_csv(data: Dict[str, Any], output_path: Optional[Path] = None) -> str:
    """Exports comprehensive multi-section project audit and metrics tables to CSV format."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Section 1: Overview
    writer.writerow(["================================================================="])
    writer.writerow(["impactx — ENTERPRISE ARCHITECTURAL AUDIT & IMPACT ASSESSMENT REPORT"])
    writer.writerow(["================================================================="])
    writer.writerow(["Project Name", data.get("project_name", "Unknown")])
    writer.writerow(["Generated Timestamp", data.get("timestamp", "")])
    health_score = data.get("health_score", 100)
    grade = "A" if health_score >= 90 else ("B" if health_score >= 80 else ("C" if health_score >= 70 else "D"))
    writer.writerow(["Architectural Health Score", f"{health_score}/100 (Grade {grade})"])
    writer.writerow(["Total Source Files", data.get("total_files", 0)])
    writer.writerow(["Total Code Lines (LOC)", data.get("total_code_lines", 0)])
    writer.writerow(["Total Lines (inc. comments/blank)", data.get("total_lines", 0)])
    writer.writerow(["Total AST Entities (Nodes)", data.get("total_nodes", 0)])
    writer.writerow(["Total Dependency Edges", data.get("total_dependencies", 0)])
    
    tot_nodes = data.get("total_nodes", 0) or 1
    tot_edges = data.get("total_dependencies", 0)
    writer.writerow(["Average Coupling Ratio", f"{tot_edges / tot_nodes:.2f} edges/node"])

    has_cycles = data.get("has_cycles", False)
    topo_str = "Clean DAG (0 Circular Dependencies)" if not has_cycles else f"WARNING: {data.get('cycles_count', 0)} Circular Dependency Cycles Detected"
    writer.writerow(["Topology Status", topo_str])
    writer.writerow(["Total Dead Code Candidates", len(data.get("unused_candidates", []))])
    writer.writerow(["Critical Risk Pruning Targets", data.get("critical_risk_unused_count", 0)])
    writer.writerow(["High Risk Pruning Targets", data.get("high_risk_unused_count", 0)])
    writer.writerow([])

    # Section 2: Language Distribution
    writer.writerow(["=== SECTION 1: LANGUAGE COMPOSITION ==="])
    writer.writerow(["Language", "File Count", "Percentage of Codebase"])
    lang_dist = data.get("language_distribution", {})
    tot_files = data.get("total_files", 0) or 1
    for lang, count in sorted(lang_dist.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([lang, count, f"{(count / tot_files) * 100:.1f}%"])
    writer.writerow([])

    # Section 3: Circular Dependencies
    writer.writerow(["=== SECTION 2: TOPOLOGY & CYCLE AUDIT ==="])
    cycles = data.get("cycles", [])
    if cycles:
        writer.writerow(["Cycle #", "Circular Path"])
        for idx, c in enumerate(cycles, start=1):
            writer.writerow([idx, " -> ".join(c) + " -> " + c[0]])
    else:
        writer.writerow(["Verified Clean DAG: No circular dependency cycles found."])
    writer.writerow([])

    # Section 4: Top Architectural Hubs
    writer.writerow(["=== SECTION 3: TOP ARCHITECTURAL HUBS (BLAST RADIUS ANALYSIS) ==="])
    writer.writerow(["Rank", "Component Identifier", "Entity Type", "PageRank", "In-Degree (Dependents)", "Out-Degree (Dependencies)", "Total Degree", "Blast Risk Tier", "Refactoring Guidance"])
    for idx, h in enumerate(data.get("top_hubs", []), start=1):
        in_deg = h.get("in_degree", 0)
        out_deg = h.get("out_degree", 0)
        risk = "CRITICAL" if in_deg >= 10 else ("HIGH" if in_deg >= 5 else ("MODERATE" if in_deg >= 2 else "LOW"))
        guidance = "Central Hub — High regression blast radius. Require regression tests." if in_deg >= 5 else "Moderate hub."
        writer.writerow([
            idx,
            h.get("id", ""),
            h.get("entity_type", ""),
            f"{h.get('pagerank', 0.0):.5f}",
            in_deg,
            out_deg,
            in_deg + out_deg,
            risk,
            guidance
        ])
    writer.writerow([])

    # Section 5: Dead Code Inventory
    writer.writerow(["=== SECTION 4: DEAD CODE & UNUSED COMPONENT INVENTORY ==="])
    writer.writerow(["Rank", "Component Name", "Entity Type", "File Location", "Incoming References", "Non-Use Confidence", "Risk Tier", "Pruning Action"])
    for idx, u in enumerate(data.get("unused_candidates", []), start=1):
        risk = str(u.get("risk_level", "LOW")).upper()
        rec = "Safe to prune (0 references across static AST)" if risk in ("CRITICAL", "HIGH") else "Review for dynamic or runtime dispatch before pruning"
        writer.writerow([
            idx,
            u.get("name", ""),
            u.get("type", ""),
            u.get("file_path", ""),
            u.get("reference_count", 0),
            f"{u.get('unused_probability', 0.0) * 100:.1f}%",
            risk,
            rec
        ])
    writer.writerow([])

    # Section 6: Safety Protocol
    writer.writerow(["=== SECTION 5: ARCHITECTURAL REFACTORING & PRUNING PROTOCOL ==="])
    writer.writerow(["1. Framework Bootstrap Entrypoints: server.js, index.html, main.jsx typically have 0 static imports. Retain unless refactoring boot sequence."])
    writer.writerow(["2. Dynamic Dispatch: Check dynamic import(), route definitions, and event bus strings prior to deleting components."])
    writer.writerow(["3. Regression Testing: Run integration test suites across the calculated downstream blast radius."])
    writer.writerow(["4. Staged Deprecation: Mark code as deprecated for 1 release cycle before physical removal."])

    csv_str = output.getvalue()
    if output_path:
        Path(output_path).write_text(csv_str, encoding="utf-8")
    return csv_str

def export_to_pdf(data: Dict[str, Any], output_path: Optional[Path] = None) -> bytes:
    """Exports a publication-grade PDF audit report using ReportLab with custom NumberedCanvas."""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas

    class NumberedCanvas(canvas.Canvas):
        """Two-pass canvas for dynamic total page count, running headers, and running footers."""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_decorations(num_pages)
                super().showPage()
            super().save()

        def draw_page_decorations(self, page_count: int):
            self.saveState()
            # Running header on pages 2+
            if self._pageNumber > 1:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor("#4F46E5"))
                self.drawString(36, 762, "impactx")
                self.setFont("Helvetica", 8)
                self.setFillColor(colors.HexColor("#64748B"))
                self.drawString(75, 762, "— Architectural & Code Change Audit Report")
                self.drawRightString(576, 762, f"Project: {data.get('project_name', 'Unknown')}")
                self.setStrokeColor(colors.HexColor("#E2E8F0"))
                self.setLineWidth(0.5)
                self.line(36, 755, 576, 755)

            # Running footer on all pages
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 34, 576, 34)
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 22, "impactx ML Architecture Intelligence Platform  •  Enterprise Code Audit  •  Confidential")
            self.drawRightString(576, 22, f"Page {self._pageNumber} of {page_count}")
            self.restoreState()

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=42,
    )
    styles = getSampleStyleSheet()

    # Custom styles
    tag_style = ParagraphStyle('BTag', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor('#818CF8'), fontName='Helvetica-Bold')
    title_style = ParagraphStyle('BTitle', parent=styles['Heading1'], fontSize=17, leading=21, textColor=colors.white, fontName='Helvetica-Bold')
    sub_style = ParagraphStyle('BSub', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor('#C7D2FE'), fontName='Helvetica')
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=10.5, leading=14, textColor=colors.HexColor('#1E1B4B'), fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=7.8, leading=11, textColor=colors.HexColor('#334155'), fontName='Helvetica')
    body_bold = ParagraphStyle('BodyB', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#1E1B4B'))
    
    kpi_val = ParagraphStyle('KVal', parent=styles['Normal'], fontSize=13, leading=15, textColor=colors.HexColor('#1E1B4B'), fontName='Helvetica-Bold', alignment=1)
    kpi_lbl = ParagraphStyle('KLbl', parent=styles['Normal'], fontSize=6.5, leading=8.5, textColor=colors.HexColor('#64748B'), fontName='Helvetica-Bold', alignment=1)
    
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.white, fontName='Helvetica-Bold')
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.HexColor('#1E293B'), fontName='Helvetica')
    td_mono = ParagraphStyle('TDM', parent=styles['Normal'], fontSize=6.5, leading=8.5, textColor=colors.HexColor('#334155'), fontName='Courier')
    
    badge_crit = ParagraphStyle('BCrit', parent=td_style, textColor=colors.HexColor('#991B1B'), fontName='Helvetica-Bold')
    badge_high = ParagraphStyle('BHigh', parent=td_style, textColor=colors.HexColor('#DC2626'), fontName='Helvetica-Bold')
    badge_med = ParagraphStyle('BMed', parent=td_style, textColor=colors.HexColor('#D97706'), fontName='Helvetica-Bold')
    badge_low = ParagraphStyle('BLow', parent=td_style, textColor=colors.HexColor('#16A34A'), fontName='Helvetica-Bold')

    story = []

    # 1. Executive Banner Table
    proj_name = data.get('project_name', 'Unknown')
    ts = data.get('timestamp', '')
    health_score = data.get('health_score', 100)
    grade = "A" if health_score >= 90 else ("B+" if health_score >= 80 else ("B" if health_score >= 70 else "C"))

    banner_data = [
        [
            Paragraph("IMPACTX ML ARCHITECTURE INTELLIGENCE  •  EXECUTIVE CODE AUDIT", tag_style),
            Paragraph(f"HEALTH SCORE: <b>{health_score}/100</b> ({grade})", ParagraphStyle('Score', parent=tag_style, alignment=2, textColor=colors.HexColor('#A7F3D0')))
        ],
        [
            Paragraph(f"Architecture &amp; Impact Audit: <b>{proj_name}</b>", title_style),
            ""
        ],
        [
            Paragraph(f"Generated: {ts} &nbsp;|&nbsp; Engine: impactx v2.1.3 ML Platform (AST Parser + Graph Centrality + XGBoost/RF)", sub_style),
            ""
        ]
    ]
    t_banner = Table(banner_data, colWidths=[390, 150])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('SPAN', (0,1), (1,1)),
        ('SPAN', (0,2), (1,2)),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 8))

    # 2. Executive Overview & 8-KPI Health Scorecard
    story.append(Paragraph("1. Executive Overview &amp; Architectural Health Scorecard", h2_style))
    has_cycles = data.get('has_cycles', False)
    topo_label = "Clean DAG (0 Cycles)" if not has_cycles else f"⚠️ {data.get('cycles_count', 0)} Cycles Detected"
    
    tot_files = data.get('total_files', 0)
    tot_loc = data.get('total_code_lines', 0)
    tot_nodes = data.get('total_nodes', 0)
    tot_edges = data.get('total_dependencies', 0)
    coupling_ratio = f"{tot_edges / (tot_nodes or 1):.2f}"
    
    crit_cnt = data.get('critical_risk_unused_count', 0)
    high_cnt = data.get('high_risk_unused_count', 0)
    prune_targets = crit_cnt + high_cnt
    tot_unused = len(data.get('unused_candidates', []))

    kpi_cards = [
        [
            [Paragraph("TOTAL SOURCE FILES", kpi_lbl), Paragraph(str(tot_files), kpi_val)],
            [Paragraph("CODE LINES (LOC)", kpi_lbl), Paragraph(f"{tot_loc:,}", kpi_val)],
            [Paragraph("GRAPH ENTITIES", kpi_lbl), Paragraph(str(tot_nodes), kpi_val)],
            [Paragraph("DEPENDENCIES", kpi_lbl), Paragraph(str(tot_edges), kpi_val)],
        ],
        [
            [Paragraph("COUPLING RATIO", kpi_lbl), Paragraph(f"{coupling_ratio}", kpi_val)],
            [Paragraph("TOPOLOGY STATUS", kpi_lbl), Paragraph(topo_label, ParagraphStyle('TStatus', parent=kpi_val, fontSize=9, textColor=colors.HexColor('#16A34A') if not has_cycles else colors.HexColor('#DC2626')))],
            [Paragraph("DEAD CODE TOTAL", kpi_lbl), Paragraph(str(tot_unused), kpi_val)],
            [Paragraph("HIGH-RISK PRUNING", kpi_lbl), Paragraph(str(prune_targets), ParagraphStyle('PVal', parent=kpi_val, textColor=colors.HexColor('#DC2626') if prune_targets > 0 else colors.HexColor('#16A34A')))],
        ]
    ]

    t_kpi = Table(kpi_cards, colWidths=[135, 135, 135, 135])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 6))

    # Language distribution breakdown
    lang_dist = data.get('language_distribution', {})
    if lang_dist:
        lang_parts = [f"<b>{k}:</b> {v} files ({(v / (tot_files or 1))*100:.1f}%)" for k, v in sorted(lang_dist.items(), key=lambda x: x[1], reverse=True)]
        story.append(Paragraph(f"<b>Language Breakdown:</b> {' &nbsp;•&nbsp; '.join(lang_parts)}", body_style))
        story.append(Spacer(1, 8))

    # 3. Top Architectural Hubs (Blast Radius Analysis)
    story.append(Paragraph("2. Top Architectural Hubs (Change Impact &amp; Blast Radius Analysis)", h2_style))
    story.append(Paragraph("Architectural hubs possess high incoming reference density. Modifying these components triggers cascading ripple effects across downstream dependents. Any refactoring here requires thorough regression test coverage.", body_style))
    story.append(Spacer(1, 4))

    hub_headers = [
        Paragraph("#", th_style),
        Paragraph("Component Identifier / Path", th_style),
        Paragraph("Type", th_style),
        Paragraph("PageRank", th_style),
        Paragraph("In (Refs)", th_style),
        Paragraph("Out (Deps)", th_style),
        Paragraph("Blast Risk Tier", th_style),
    ]
    hub_rows = [hub_headers]
    hubs_to_show = data.get('top_hubs', [])[:28]
    for idx, h in enumerate(hubs_to_show, start=1):
        in_deg = h.get('in_degree', 0)
        out_deg = h.get('out_degree', 0)
        risk = "CRITICAL" if in_deg >= 10 else ("HIGH" if in_deg >= 5 else ("MODERATE" if in_deg >= 2 else "LOW"))
        r_style = badge_crit if risk == "CRITICAL" else (badge_high if risk == "HIGH" else (badge_med if risk == "MODERATE" else badge_low))

        hub_rows.append([
            Paragraph(f"#{idx}", td_style),
            Paragraph(_break_path(str(h.get('id', ''))), td_mono),
            Paragraph(str(h.get('entity_type', 'file')), td_style),
            Paragraph(f"{h.get('pagerank', 0.0):.4f}", td_style),
            Paragraph(str(in_deg), td_style),
            Paragraph(str(out_deg), td_style),
            Paragraph(risk, r_style),
        ])

    if len(hub_rows) > 1:
        t_hubs = Table(hub_rows, colWidths=[24, 230, 56, 60, 50, 50, 70])
        t_hubs.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E1B4B')),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (2,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_hubs)
    else:
        story.append(Paragraph("No high-risk architectural hubs detected.", body_style))
    story.append(Spacer(1, 10))

    # 4. Dead Code & Unused Component Inventory
    story.append(Paragraph("3. Dead Code &amp; Unused Component Inventory", h2_style))
    story.append(Paragraph("Components identified with zero incoming references across the static AST dependency graph, validated by ML heuristic confidence. These candidates represent potential dead code, obsolete features, or orphaned utilities.", body_style))
    story.append(Spacer(1, 4))

    unused_headers = [
        Paragraph("#", th_style),
        Paragraph("Component Name", th_style),
        Paragraph("Type", th_style),
        Paragraph("File Path Location", th_style),
        Paragraph("Refs", th_style),
        Paragraph("Non-Use Prob", th_style),
        Paragraph("Risk Tier", th_style),
    ]
    unused_rows = [unused_headers]
    unused_to_show = data.get('unused_candidates', [])[:45]
    for idx, u in enumerate(unused_to_show, start=1):
        risk = str(u.get('risk_level', 'LOW')).upper()
        r_style = badge_crit if risk == 'CRITICAL' else (badge_high if risk == 'HIGH' else (badge_med if risk == 'MEDIUM' else badge_low))

        unused_rows.append([
            Paragraph(f"#{idx}", td_style),
            Paragraph(_break_path(str(u.get('name', ''))), td_mono),
            Paragraph(str(u.get('type', 'file')), td_style),
            Paragraph(_break_path(str(u.get('file_path', ''))), td_mono),
            Paragraph(str(u.get('reference_count', 0)), td_style),
            Paragraph(f"{u.get('unused_probability', 0.0) * 100:.1f}%", td_style),
            Paragraph(risk, r_style),
        ])

    if len(unused_rows) > 1:
        t_unused = Table(unused_rows, colWidths=[24, 116, 50, 195, 35, 60, 60])
        t_unused.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E1B4B')),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (2,0), (2,-1), 'CENTER'),
            ('ALIGN', (4,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_unused)
    else:
        story.append(Paragraph("No unused code candidates detected.", body_style))
    story.append(Spacer(1, 10))

    # 5. Circular Dependency Detection & Remediation
    story.append(KeepTogether([
        Paragraph("4. Circular Dependency Audit &amp; Topology Verification", h2_style),
        Paragraph(
            "Circular dependencies occur when components mutually require each other directly or transitively. Circular loops severely degrade testability, prevent tree-shaking, and create fragile tight coupling.",
            body_style
        ),
        Spacer(1, 3)
    ]))
    cycles = data.get("cycles", [])
    if cycles:
        cycle_paras = []
        for idx, c in enumerate(cycles[:6], start=1):
            cycle_str = " &rarr; ".join(c) + f" &rarr; {c[0]}"
            cycle_paras.append(Paragraph(f"<b>Loop #{idx}:</b> <code>{cycle_str}</code>", body_style))
        story.append(KeepTogether(cycle_paras))
    else:
        story.append(Paragraph("<b>✓ Pure Directed Acyclic Graph (DAG) Verified:</b> No circular dependency loops detected. The codebase architecture adheres to clean hierarchical dependency layers.", body_style))
    story.append(Spacer(1, 8))

    # 6. Safety Protocol
    story.append(KeepTogether([
        Paragraph("5. Architectural Refactoring &amp; Pruning Protocol", h2_style),
        Paragraph("<b>1. Framework Bootstrap Roots:</b> Server and web entrypoints (e.g. server.js, index.html, main.jsx, App.tsx) typically have 0 incoming static imports because they are initiated directly by the runtime environment. Retain unless refactoring the bootstrap sequence.", body_style),
        Spacer(1, 2),
        Paragraph("<b>2. Dynamic String References:</b> Search the codebase for dynamic <code>import()</code> calls, route definitions, template strings, or event bus channel keys prior to deleting modules.", body_style),
        Spacer(1, 2),
        Paragraph("<b>3. Blast Radius Regression Testing:</b> Execute automated end-to-end and integration test suites across all downstream dependents identified in Section 2 before committing deletions.", body_style),
        Spacer(1, 2),
        Paragraph("<b>4. Staged Deprecation:</b> Annotate candidate components as <code>@deprecated</code> and monitor production telemetry for 1 release cycle before physical removal.", body_style),
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    pdf_bytes = buf.getvalue()
    if output_path:
        Path(output_path).write_bytes(pdf_bytes)
    return pdf_bytes

def export_to_docx(data: Dict[str, Any], output_path: Optional[Path] = None) -> bytes:
    """Exports an executive-level Word document (.docx) audit report using python-docx."""
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls

    doc = Document()

    # Margins: 0.75 in
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        # Header
        p_head = section.header.paragraphs[0]
        p_head.text = f"impactx — Architecture Intelligence Audit  |  Project: {data.get('project_name', 'Unknown')}"
        p_head.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        p_head.runs[0].font.size = Pt(8)
        p_head.runs[0].font.color.rgb = RGBColor(148, 163, 184)

        # Footer
        p_foot = section.footer.paragraphs[0]
        p_foot.text = "Confidential  •  Generated by impactx ML Platform"
        p_foot.runs[0].font.size = Pt(8)
        p_foot.runs[0].font.color.rgb = RGBColor(148, 163, 184)

    navy = RGBColor(30, 27, 75)
    indigo = RGBColor(79, 70, 229)
    slate = RGBColor(100, 116, 139)

    # Document Header Tag
    p_tag = doc.add_paragraph()
    r_tag = p_tag.add_run("IMPACTX ARCHITECTURAL AUDIT REPORT")
    r_tag.font.size = Pt(8.5)
    r_tag.font.bold = True
    r_tag.font.color.rgb = indigo
    p_tag.paragraph_format.space_after = Pt(2)

    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run(f"Architecture & Code Change Audit: {data.get('project_name', 'Unknown')}")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = navy
    p_title.paragraph_format.space_after = Pt(2)

    # Subtitle
    health_score = data.get('health_score', 100)
    grade = "A" if health_score >= 90 else ("B+" if health_score >= 80 else ("B" if health_score >= 70 else "C"))
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run(f"Health Score: {health_score}/100 (Grade {grade})  |  Generated: {data.get('timestamp', '')}  |  Engine: impactx v2.1.3")
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = slate
    p_sub.paragraph_format.space_after = Pt(12)

    # Section 1: Executive Overview & Scorecard
    h1 = doc.add_heading(level=1)
    h1_r = h1.add_run("1. Executive Overview & Architectural Health Scorecard")
    h1_r.font.color.rgb = navy
    h1.paragraph_format.space_before = Pt(10)
    h1.paragraph_format.space_after = Pt(6)

    has_cycles = data.get("has_cycles", False)
    topo_text = "Clean DAG (0 Circular Cycles)" if not has_cycles else f"WARNING: {data.get('cycles_count', 0)} Cycles Detected"
    
    tot_files = data.get('total_files', 0)
    tot_loc = data.get('total_code_lines', 0)
    tot_nodes = data.get('total_nodes', 0)
    tot_edges = data.get('total_dependencies', 0)
    coupling_ratio = f"{tot_edges / (tot_nodes or 1):.2f}"
    prune_cnt = data.get("critical_risk_unused_count", 0) + data.get("high_risk_unused_count", 0)
    tot_unused = len(data.get("unused_candidates", []))

    # KPI Table (2 rows x 4 cols)
    kpi_table = doc.add_table(rows=2, cols=4)
    kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_items = [
        ("Total Files", str(tot_files)),
        ("Code LOC", f"{tot_loc:,}"),
        ("AST Entities", str(tot_nodes)),
        ("Dependencies", str(tot_edges)),
        ("Coupling Ratio", coupling_ratio),
        ("Topology Status", topo_text),
        ("Dead Code Total", str(tot_unused)),
        ("High-Risk Pruning", str(prune_cnt)),
    ]
    for idx, (label, val) in enumerate(kpi_items):
        row_idx = idx // 4
        col_idx = idx % 4
        cell = kpi_table.cell(row_idx, col_idx)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_l = p.add_run(f"{label}:\n")
        r_l.font.bold = True
        r_l.font.size = Pt(8)
        r_l.font.color.rgb = slate
        r_v = p.add_run(val)
        r_v.font.bold = True
        r_v.font.size = Pt(9.5)
        if "WARNING" in val:
            r_v.font.color.rgb = RGBColor(220, 38, 38)
        else:
            r_v.font.color.rgb = navy
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Language breakdown
    lang_dist = data.get("language_distribution", {})
    if lang_dist:
        p_lang = doc.add_paragraph()
        p_lang.paragraph_format.space_after = Pt(10)
        r_lang_lbl = p_lang.add_run("Language Composition: ")
        r_lang_lbl.font.bold = True
        r_lang_lbl.font.size = Pt(9)
        lang_parts = [f"{k} ({v} files, {(v / (tot_files or 1))*100:.1f}%)" for k, v in sorted(lang_dist.items(), key=lambda x: x[1], reverse=True)]
        p_lang.add_run("  •  ".join(lang_parts)).font.size = Pt(9)

    # Section 2: Top Architectural Hubs
    h2 = doc.add_heading(level=1)
    h2_r = h2.add_run("2. Top Architectural Hubs (Highest Blast Radius / Risk)")
    h2_r.font.color.rgb = navy
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)

    hubs = data.get("top_hubs", [])
    if hubs:
        t_hub = doc.add_table(rows=1, cols=7)
        t_hub.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["#", "Component ID", "Type", "PageRank", "In (Refs)", "Out (Deps)", "Blast Risk"]
        for i, h_text in enumerate(headers):
            cell = t_hub.cell(0, i)
            cell.paragraphs[0].text = h_text
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E1B4B"/>')
            cell._tc.get_or_add_tcPr().append(shd)

        for idx, h in enumerate(hubs[:30], start=1):
            row = t_hub.add_row()
            in_deg = h.get("in_degree", 0)
            out_deg = h.get("out_degree", 0)
            risk = "CRITICAL" if in_deg >= 10 else ("HIGH" if in_deg >= 5 else ("MODERATE" if in_deg >= 2 else "LOW"))
            vals = [
                f"#{idx}",
                str(h.get("id", "")),
                str(h.get("entity_type", "file")),
                f"{h.get('pagerank', 0.0):.4f}",
                str(in_deg),
                str(out_deg),
                risk,
            ]
            for j, val in enumerate(vals):
                c = row.cells[j]
                c.paragraphs[0].text = val
                r = c.paragraphs[0].runs[0]
                r.font.size = Pt(7.5)
                if j == 6:
                    r.font.bold = True
                    if risk == "CRITICAL":
                        r.font.color.rgb = RGBColor(153, 27, 27)
                    elif risk == "HIGH":
                        r.font.color.rgb = RGBColor(220, 38, 38)
                    elif risk == "MODERATE":
                        r.font.color.rgb = RGBColor(217, 119, 6)
                    else:
                        r.font.color.rgb = RGBColor(22, 163, 74)
    else:
        p_nohub = doc.add_paragraph("No architectural hubs detected.")
        p_nohub.runs[0].font.size = Pt(9)

    # Section 3: Dead Code Candidates
    h3 = doc.add_heading(level=1)
    h3_r = h3.add_run("3. Dead Code & Unused Component Inventory")
    h3_r.font.color.rgb = navy
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

    unused = data.get("unused_candidates", [])
    if unused:
        t_un = doc.add_table(rows=1, cols=7)
        t_un.alignment = WD_TABLE_ALIGNMENT.CENTER
        u_headers = ["#", "Component Name", "Type", "File Location", "Refs", "Unused Prob", "Risk Tier"]
        for i, u_text in enumerate(u_headers):
            cell = t_un.cell(0, i)
            cell.paragraphs[0].text = u_text
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E1B4B"/>')
            cell._tc.get_or_add_tcPr().append(shd)

        for idx, u in enumerate(unused[:45], start=1):
            row = t_un.add_row()
            risk = str(u.get("risk_level", "LOW")).upper()
            vals = [
                f"#{idx}",
                str(u.get("name", "")),
                str(u.get("type", "file")),
                str(u.get("file_path", "")),
                str(u.get("reference_count", 0)),
                f"{u.get('unused_probability', 0.0) * 100:.1f}%",
                risk,
            ]
            for j, val in enumerate(vals):
                c = row.cells[j]
                c.paragraphs[0].text = val
                r = c.paragraphs[0].runs[0]
                r.font.size = Pt(7.5)
                if j == 6:
                    r.font.bold = True
                    if risk == "CRITICAL":
                        r.font.color.rgb = RGBColor(153, 27, 27)
                    elif risk == "HIGH":
                        r.font.color.rgb = RGBColor(220, 38, 38)
                    elif risk == "MEDIUM":
                        r.font.color.rgb = RGBColor(217, 119, 6)
                    else:
                        r.font.color.rgb = RGBColor(22, 163, 74)
    else:
        p_noun = doc.add_paragraph("No unused code candidates detected.")
        p_noun.runs[0].font.size = Pt(9)

    # Section 4: Refactoring Protocol
    h4 = doc.add_heading(level=1)
    h4_r = h4.add_run("4. Architectural Refactoring & Safety Checklist")
    h4_r.font.color.rgb = navy
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    guidelines = [
        "1. Preserve Framework Bootstrap Roots: Server and web bootstrap entrypoints (server.js, main.jsx, index.html) must not be deleted even if they have 0 static imports.",
        "2. Dynamic & Route References: Search codebase for dynamic imports, string-based route paths, and configuration files before deletion.",
        "3. Integration Testing: Run regression tests on all consumers connected through the dependency network.",
        "4. Staged Deprecation: Mark code as deprecated for one release cycle before full removal.",
    ]
    for g in guidelines:
        p_g = doc.add_paragraph(g)
        p_g.paragraph_format.space_after = Pt(3)
        p_g.runs[0].font.size = Pt(8.5)

    buf = io.BytesIO()
    doc.save(buf)
    docx_bytes = buf.getvalue()
    if output_path:
        Path(output_path).write_bytes(docx_bytes)
    return docx_bytes

def export_to_html(data: Dict[str, Any], output_path: Optional[Path] = None, theme: str = "dark") -> str:
    """Exports a self-contained, beautifully styled HTML report matching the impactx theme."""
    is_dark = (theme.lower() == "dark")

    bg_color = "#080D1A" if is_dark else "#F8FAFC"
    card_bg = "#0E131F" if is_dark else "#FFFFFF"
    text_color = "#FFFFFF" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#64748B"
    border_color = "rgba(255, 255, 255, 0.08)" if is_dark else "#E2E8F0"
    badge_bg = "rgba(99, 102, 241, 0.15)" if is_dark else "rgba(99, 102, 241, 0.1)"
    badge_color = "#A5B4FC" if is_dark else "#4F46E5"
    table_header_bg = "#161B28" if is_dark else "#F1F5F9"

    # Hub rows
    hub_rows = ""
    for idx, h in enumerate(data.get("top_hubs", [])[:30], start=1):
        in_deg = h.get("in_degree", 0)
        risk = "CRITICAL" if in_deg >= 10 else ("HIGH" if in_deg >= 5 else ("MODERATE" if in_deg >= 2 else "LOW"))
        risk_color = "#DC2626" if risk == "CRITICAL" else ("#EF4444" if risk == "HIGH" else ("#F59E0B" if risk == "MODERATE" else "#10B981"))

        hub_rows += f"""
        <tr>
            <td style="color: {sub_color}; font-family: monospace;">#{idx}</td>
            <td style="font-weight: 600; font-family: monospace; font-size: 12px;">{h.get('id')}</td>
            <td><span class="badge">{h.get('entity_type', 'file')}</span></td>
            <td>{h.get('pagerank', 0.0):.4f}</td>
            <td style="font-weight: 700;">{in_deg}</td>
            <td>{h.get('out_degree', 0)}</td>
            <td><span style="color: {risk_color}; font-weight: 700; font-size: 11px;">{risk}</span></td>
        </tr>
        """

    # Dead code rows
    unused_rows = ""
    for idx, u in enumerate(data.get("unused_candidates", [])[:50], start=1):
        risk = str(u.get("risk_level", "LOW")).upper()
        if risk == "CRITICAL":
            risk_color = "#DC2626"
        elif risk == "HIGH":
            risk_color = "#EF4444"
        elif risk == "MEDIUM":
            risk_color = "#F59E0B"
        else:
            risk_color = "#10B981"

        prob = u.get('unused_probability', 0.0) * 100
        unused_rows += f"""
        <tr>
            <td style="color: {sub_color}; font-family: monospace;">#{idx}</td>
            <td style="font-weight: 600; font-family: monospace; font-size: 12px;">{u.get('name')}</td>
            <td><span class="badge">{u.get('type', 'file')}</span></td>
            <td style="color: {sub_color}; font-size: 12px; font-family: monospace;">{u.get('file_path')}</td>
            <td style="text-align: center; font-weight: 700;">{u.get('reference_count', 0)}</td>
            <td>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="flex: 1; height: 5px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;">
                        <div style="width: {prob}%; height: 100%; background: {risk_color};"></div>
                    </div>
                    <span style="font-size: 11px; font-family: monospace;">{prob:.1f}%</span>
                </div>
            </td>
            <td><span style="color: {risk_color}; font-weight: 700; font-size: 11px;">{risk}</span></td>
        </tr>
        """

    has_cycles = data.get("has_cycles", False)
    topo_text = "Clean DAG (0 Circular Cycles)" if not has_cycles else f"⚠️ {data.get('cycles_count', 0)} Circular Cycles Detected"
    topo_color = "#10B981" if not has_cycles else "#EF4444"

    tot_files = data.get("total_files", 0)
    tot_loc = data.get("total_code_lines", 0)
    tot_nodes = data.get("total_nodes", 0)
    tot_edges = data.get("total_dependencies", 0)
    crit_prune = data.get("critical_risk_unused_count", 0) + data.get("high_risk_unused_count", 0)
    health_score = data.get("health_score", 100)
    grade = "A" if health_score >= 90 else ("B+" if health_score >= 80 else ("B" if health_score >= 70 else "C"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>impactx — Architecture &amp; Impact Audit Report ({data.get('project_name', 'Unknown')})</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 40px 24px;
            background-color: {bg_color};
            color: {text_color};
            font-family: 'Inter', system-ui, sans-serif;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .hero {{
            padding: 32px 30px;
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(14, 19, 31, 0.95) 100%);
            border-radius: 16px;
            margin-bottom: 28px;
            border: 1px solid {border_color};
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .hero-left {{ flex: 1; min-width: 300px; }}
        .hero-pill {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            background: {badge_bg};
            color: {badge_color};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            border: 1px solid rgba(139, 92, 246, 0.3);
            margin-bottom: 12px;
        }}
        h1 {{
            font-size: 26px;
            font-weight: 800;
            margin: 0 0 8px 0;
            letter-spacing: -0.5px;
            color: #FFFFFF;
        }}
        .subtitle {{
            color: {sub_color};
            font-size: 13px;
        }}
        .health-badge {{
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 16px 24px;
            text-align: center;
        }}
        .health-score {{
            font-size: 32px;
            font-weight: 800;
            color: #10B981;
            line-height: 1;
        }}
        .health-lbl {{
            font-size: 11px;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            margin-top: 4px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 14px;
            margin-bottom: 28px;
        }}
        .card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .card-val {{
            font-size: 24px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 6px;
            line-height: 1.1;
        }}
        .card-lbl {{
            color: {sub_color};
            font-size: 10.5px;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.6px;
        }}
        .card-sub {{
            font-size: 11px;
            color: #64748B;
            margin-top: 4px;
        }}
        .section-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.25);
        }}
        .section-card h2 {{
            font-size: 17px;
            font-weight: 700;
            margin: 0 0 4px 0;
            color: #FFFFFF;
        }}
        .section-card p {{
            font-size: 12px;
            color: {sub_color};
            margin: 0 0 14px 0;
        }}
        .table-wrap {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 9px 12px;
            text-align: left;
            border-bottom: 1px solid {border_color};
            font-size: 12px;
        }}
        th {{
            background: {table_header_bg};
            color: {sub_color};
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}
        .badge {{
            padding: 2px 7px;
            border-radius: 4px;
            background: {badge_bg};
            color: {badge_color};
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .checklist-item {{
            display: flex;
            gap: 12px;
            margin-bottom: 12px;
            font-size: 12.5px;
        }}
        .checklist-num {{
            font-weight: 700;
            color: #6366F1;
            font-family: monospace;
        }}
        @media print {{
            body {{ background-color: #FFFFFF; color: #0F172A; padding: 20px; }}
            .hero {{ background: #F8FAFC; border: 1px solid #CBD5E1; color: #0F172A; }}
            h1, .section-card h2 {{ color: #0F172A; }}
            .card, .section-card {{ background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: none; }}
            .card-val {{ color: #0F172A; }}
            th {{ background: #F1F5F9; color: #475569; }}
            td {{ color: #1E293B; border-bottom: 1px solid #E2E8F0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Header -->
        <div class="hero">
            <div class="hero-left">
                <div class="hero-pill">impactx Architecture Intelligence</div>
                <h1>Codebase Architecture &amp; Impact Audit</h1>
                <div class="subtitle">
                    Project: <strong style="color: #FFFFFF;">{data.get("project_name", "Unknown")}</strong> &nbsp;|&nbsp; 
                    Generated: {data.get("timestamp", "")} &nbsp;|&nbsp; 
                    Engine: impactx v2.1.3 ML Platform
                </div>
            </div>
            <div class="health-badge">
                <div class="health-score">{health_score}<span style="font-size: 18px;">/100</span></div>
                <div class="health-lbl">Health Grade: {grade}</div>
            </div>
        </div>

        <!-- 8 KPI Scorecard Grid -->
        <div class="grid">
            <div class="card">
                <div class="card-lbl">Total Source Files</div>
                <div class="card-val">{tot_files}</div>
                <div class="card-sub">Cataloged files</div>
            </div>
            <div class="card">
                <div class="card-lbl">Code Lines (LOC)</div>
                <div class="card-val">{tot_loc:,}</div>
                <div class="card-sub">Effective syntax lines</div>
            </div>
            <div class="card">
                <div class="card-lbl">AST Entities</div>
                <div class="card-val">{tot_nodes}</div>
                <div class="card-sub">Nodes in dependency graph</div>
            </div>
            <div class="card">
                <div class="card-lbl">Graph Dependencies</div>
                <div class="card-val">{tot_edges}</div>
                <div class="card-sub">Directed import edges</div>
            </div>
            <div class="card">
                <div class="card-lbl">Coupling Ratio</div>
                <div class="card-val">{tot_edges / (tot_nodes or 1):.2f}</div>
                <div class="card-sub">Dependencies / Entity</div>
            </div>
            <div class="card">
                <div class="card-lbl">Topology Status</div>
                <div class="card-val" style="font-size: 15px; color: {topo_color}; margin-top: 8px;">{topo_text}</div>
                <div class="card-sub">Cycle audit</div>
            </div>
            <div class="card">
                <div class="card-lbl">Dead Code Candidates</div>
                <div class="card-val">{len(data.get("unused_candidates", []))}</div>
                <div class="card-sub">Unreferenced entities</div>
            </div>
            <div class="card">
                <div class="card-lbl">High-Risk Pruning</div>
                <div class="card-val" style="color: #EF4444;">{crit_prune}</div>
                <div class="card-sub">Priority removal targets</div>
            </div>
        </div>

        <!-- Section: Top Hubs -->
        <div class="section-card">
            <h2>Top Architectural Hubs (Blast Radius Analysis)</h2>
            <p>Components with the highest incoming reference density and PageRank. Changes to these hubs ripple across downstream dependants.</p>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 40px;">Rank</th>
                            <th>Component ID</th>
                            <th>Type</th>
                            <th>PageRank</th>
                            <th>In-Degree (Refs)</th>
                            <th>Out-Degree</th>
                            <th>Blast Risk</th>
                        </tr>
                    </thead>
                    <tbody>
                        {hub_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Section: Dead Code -->
        <div class="section-card">
            <h2>Dead Code &amp; Unused Component Inventory</h2>
            <p>Catalog of components identified with zero incoming references and high ML confidence scoring for safe code pruning.</p>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 40px;">Rank</th>
                            <th>Component Name</th>
                            <th>Type</th>
                            <th>File Path</th>
                            <th style="text-align: center;">Refs</th>
                            <th style="width: 140px;">Non-Use Prob</th>
                            <th>Risk Tier</th>
                        </tr>
                    </thead>
                    <tbody>
                        {unused_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Section: Safety Checklist -->
        <div class="section-card">
            <h2>Architectural Refactoring &amp; Pruning Protocol</h2>
            <p>Standard operating guidelines for safely retiring unused code and refactoring dependency hubs.</p>
            
            <div class="checklist-item">
                <div class="checklist-num">01.</div>
                <div><strong>Preserve Framework Bootstrap Roots:</strong> Server and web entrypoints (e.g. server.js, index.html, main.jsx) often possess 0 incoming static imports because they are initiated directly by the runtime environment.</div>
            </div>
            <div class="checklist-item">
                <div class="checklist-num">02.</div>
                <div><strong>Dynamic Import Inspection:</strong> Search for string references, dynamic <code>import()</code> calls, route definitions, or dependency injection keys prior to deleting modules.</div>
            </div>
            <div class="checklist-item">
                <div class="checklist-num">03.</div>
                <div><strong>Automated Regression Suite:</strong> Execute all unit and integration tests across the calculated downstream blast radius before committing deletions.</div>
            </div>
            <div class="checklist-item">
                <div class="checklist-num">04.</div>
                <div><strong>Graceful Deprecation Cycle:</strong> Annotate components as deprecated for 1 release cycle before physical removal from the repository.</div>
            </div>
        </div>
    </div>
</body>
</html>"""

    if output_path:
        Path(output_path).write_text(html, encoding="utf-8")
    return html
